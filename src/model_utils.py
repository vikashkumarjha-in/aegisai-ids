import os
import joblib

MODEL_DIR = "../models"
MODEL_PATH = "../models/ids_model.pkl"

def save_model(model):
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved at {MODEL_PATH}")

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Trained model not found. Train the model first.")
    print("Loading trained model...")
    return joblib.load(MODEL_PATH)
