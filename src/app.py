from fastapi.responses import HTMLResponse

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

from src.feature_engineering import create_ids_features

MODEL_PATH = "models/latest_model.pkl"

app = FastAPI(
    title="AegisAI IDS API",
    version="1.0"
)

# Load trained model
model = joblib.load(MODEL_PATH)


class TrafficInput(BaseModel):
    src_bytes: int
    dst_bytes: int
    count: int


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>AegisAI IDS</title>

            <style>
                body {
                    background-color: #0f172a;
                    color: white;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }

                .container {
                    text-align: center;
                    background: #111827;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 0 20px rgba(0,255,255,0.2);
                }

                h1 {
                    color: #38bdf8;
                    margin-bottom: 10px;
                }

                p {
                    color: #cbd5e1;
                }

                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background: #38bdf8;
                    color: black;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                }

                a:hover {
                    background: #0ea5e9;
                }
            </style>
        </head>

        <body>
            <div class="container">
                <h1>🛡️ AegisAI IDS</h1>

                <p>
                    AI-Powered Intrusion Detection System
                </p>

                <p>
                    FastAPI • Machine Learning • Cybersecurity
                </p>

                <a href="/docs">
                    Open API Documentation
                </a>
            </div>
        </body>
    </html>
    """


@app.post("/predict")
def predict(data: TrafficInput):

    raw_df = pd.DataFrame([{
        "src_bytes": data.src_bytes,
        "dst_bytes": data.dst_bytes,
        "count": data.count,
        "label": 0
    }])

    X, _ = create_ids_features(raw_df)

    prediction = int(model.predict(X)[0])

    result = "attack" if prediction == 1 else "normal"

    return {
        "prediction": result
    }