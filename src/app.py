import os
import csv
import logging
from datetime import datetime

import joblib

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    HTTPException,
    Security,
    status,
    Depends
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import APIKeyHeader

from pydantic import BaseModel, Field

from src.alert_logic import generate_alert

# ==================================================
# LOAD ENV VARIABLES
# ==================================================

load_dotenv()

# ==================================================
# BASE DIRECTORY
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "latest_model.pkl"
)

AUDIT_LOG = os.path.join(
    BASE_DIR,
    "logs",
    "audit.csv"
)

# ==================================================
# LOGGING
# ==================================================

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("aegisai.api")

# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(
    title="AegisAI IDS",
    version="1.0"
)

# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[

        "http://localhost:8501",

        "http://127.0.0.1:8501"

    ],

    allow_methods=["*"],

    allow_headers=["*"],
)

# ==================================================
# API KEY SECURITY
# ==================================================

API_KEY = os.getenv(
    "AEGISAI_API_KEY",
    "aegisai_secure_key_2026"
)

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)

def verify_api_key(
    key: str = Security(api_key_header)
):

    if key != API_KEY:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Invalid API Key"
        )

    return key

# ==================================================
# INPUT MODEL
# ==================================================

class TrafficInput(BaseModel):

    src_bytes: int = Field(
        ge=0,
        le=10_000_000
    )

    dst_bytes: int = Field(
        ge=0,
        le=10_000_000
    )

    count: int = Field(
        ge=0,
        le=65535
    )

# ==================================================
# LOAD ML MODEL
# ==================================================

model = None

try:

    if os.path.exists(MODEL_PATH):

        model = joblib.load(MODEL_PATH)

        logger.info("Model loaded successfully")

    else:

        logger.warning("Model file not found")

except Exception as e:

    logger.error(f"Model loading failed: {e}")

# ==================================================
# AUDIT LOGGING
# ==================================================

def log_prediction(
    features: dict,
    prediction: str
):

    os.makedirs(
        os.path.dirname(AUDIT_LOG),
        exist_ok=True
    )

    file_exists = os.path.exists(AUDIT_LOG)

    with open(
        AUDIT_LOG,
        "a",
        newline=""
    ) as f:

        writer = csv.DictWriter(

            f,

            fieldnames=[

                "timestamp",

                "src_bytes",

                "dst_bytes",

                "count",

                "prediction"
            ]
        )

        if not file_exists:

            writer.writeheader()

        writer.writerow({

            "timestamp":
                datetime.utcnow().isoformat(),

            **features,

            "prediction":
                prediction
        })

# ==================================================
# HEALTH ENDPOINT
# ==================================================

@app.get("/health")

def health():

    return {

        "status": "online",

        "model_loaded":
            model is not None,

        "model_path":
            MODEL_PATH
    }

# ==================================================
# PREDICT ENDPOINT
# ==================================================

@app.post(
    "/predict",

    dependencies=[Depends(verify_api_key)]
)

def predict(
    data: TrafficInput
):

    features = {

        "src_bytes":
            data.src_bytes,

        "dst_bytes":
            data.dst_bytes,

        "count":
            data.count
    }

    # ==============================================
    # AI / IDS LOGIC
    # ==============================================

    prediction_label = "normal"

    if data.count > 400:

        prediction_label = "attack"

    if data.src_bytes > 4000:

        prediction_label = "attack"

    # ==============================================
    # ALERT GENERATION
    # ==============================================

    alert = generate_alert(
        prediction_label,
        features
    )

    # ==============================================
    # LOGGING
    # ==============================================

    logger.info(
        f"Prediction: {prediction_label} | {features}"
    )

    # ==============================================
    # AUDIT LOGGING
    # ==============================================

    log_prediction(
        features,
        prediction_label
    )

    # ==============================================
    # RESPONSE
    # ==============================================

    return {

        "prediction":
            prediction_label,

        "alert":
            alert
    }