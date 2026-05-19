# src/evaluate_model.py

import sys
import os
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
from model_utils import load_model

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ===============================
# PATH CONFIGURATION
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed_nslkdd.csv")


def evaluate_model():
    print("Loading model...")
    model = load_model()

    print("Loading evaluation dataset...")
    df = pd.read_csv(DATA_PATH)

    # ===============================
    # FEATURE SECTION (updated)
    # ===============================
    feature_cols = [c for c in df.columns if c != "label"]
    X = df[feature_cols]
    y = df["label"]

    print("Running predictions...")
    y_pred = model.predict(X)

    print("\nAccuracy:", accuracy_score(y, y_pred))
    print("\nClassification Report:")
    print(classification_report(y, y_pred))


if __name__ == "__main__":
    evaluate_model()
