from fastapi import FastAPI
import joblib
import pandas as pd

# MODEL_PATH relative to project root
MODEL_PATH = "models/ids_model_v4.pkl"

app = FastAPI(title="AegisAI IDS API", version="1.0")

# load the trained pipeline (scaler + model) once
pipeline = joblib.load(MODEL_PATH)


@app.get("/")
def home():
    return {"status": "AegisAI IDS API is running"}


@app.post("/predict")
def predict(data: dict):
    """
    Accepts JSON with keys:
    {
      "packet_ratio": float,
      "high_activity": int
    }
    """
    # normalize input to DataFrame with same columns the model expects
    df = pd.DataFrame([data])
    pred = pipeline.predict(df)[0]
    return {"prediction": "attack" if int(pred) == 1 else "normal"}
