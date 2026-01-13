import pandas as pd
import os
import joblib
from sklearn.linear_model import LogisticRegression

DATA_PATH = "../data/processed_data.csv"
MODEL_DIR = "../models"
MODEL_PATH = "../models/ids_model.pkl"

def load_data():
    print("📥 Loading processed dataset...")
    data = pd.read_csv(DATA_PATH)

    if "label" not in data.columns:
        raise ValueError("❌ 'label' column not found in dataset")

    X = data.drop("label", axis=1)
    y = data["label"]

    if y.nunique() < 2:
        raise ValueError("❌ Dataset must contain at least 2 classes")

    print("✅ Dataset loaded successfully")
    return X, y

def train_model(X, y):
    print("🧠 Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    print("✅ Model training completed")
    return model

def save_model(model):
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"💾 Model saved at {MODEL_PATH}")

if __name__ == "__main__":
    X, y = load_data()
    model = train_model(X, y)
    save_model(model)

    print("🎯 Day 10 – Training step completed successfully")
