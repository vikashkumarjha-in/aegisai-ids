import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report

DATA_PATH = "../data/processed_data.csv"
MODEL_PATH = "../models/ids_model.pkl"

def load_data():
    print("📥 Loading dataset for evaluation...")
    data = pd.read_csv(DATA_PATH)

    X = data.drop("label", axis=1)
    y = data["label"]

    return X, y

def load_model():
    print("📦 Loading trained model...")
    return joblib.load(MODEL_PATH)

def evaluate_model(model, X, y):
    print("📊 Evaluating model...")
    predictions = model.predict(X)

    acc = accuracy_score(y, predictions)
    print(f"\n✅ Model Accuracy: {acc:.2f}\n")
    print("📄 Classification Report:")
    print(classification_report(y, predictions))

if __name__ == "__main__":
    X, y = load_data()
    model = load_model()
    evaluate_model(model, X, y)

    print("🎯 Day 10 – Evaluation step completed successfully")
