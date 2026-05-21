from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

app = FastAPI(title="AegisAI IDS API")

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "AegisAI IDS Backend Running",
        "status": "online"
    }

# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "backend": "online",
        "model_status": "active",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# =========================================================
# MOCK IDS PREDICTION
# =========================================================

ATTACKS = [
    "Benign",
    "DDoS",
    "Port Scan",
    "Brute Force",
    "Botnet",
    "Web Attack",
    "Infiltration"
]

SEVERITY = {
    "Benign": "Low",
    "DDoS": "Critical",
    "Port Scan": "Medium",
    "Brute Force": "High",
    "Botnet": "Critical",
    "Web Attack": "High",
    "Infiltration": "Critical"
}

@app.get("/predict")
def predict():

    attack = random.choice(ATTACKS)

    return {
        "prediction": attack,
        "severity": SEVERITY[attack],
        "confidence": round(random.uniform(88, 99), 2),
        "blocked": random.choice([True, False]),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }