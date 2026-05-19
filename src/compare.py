# src/compare.py

import sys
import os
import pandas as pd
from model_utils import load_model
from rule_based import rule_predict
from sklearn.metrics import classification_report, accuracy_score

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ===============================
# PATH CONFIGURATION
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed_nslkdd.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "latest_model.pkl")


def compare():
    print("Loading evaluation dataset...")
    df = pd.read_csv(DATA_PATH)

    # ===============================
    # FEATURE SECTION (updated)
    # ===============================
    feature_cols = [c for c in df.columns if c != "label"]
    X = df[feature_cols]
    y = df["label"]

    print("Loading ML model...")
    model = load_model()

    print("Running predictions...")
    ml_preds = model.predict(X)
    rule_preds = rule_predict(X)

    print("\n=== ML Model Results ===")
    print("Accuracy:", accuracy_score(y, ml_preds))
    print(classification_report(y, ml_preds, zero_division=0))

    print("\n=== Rule-based Results ===")
    print("Accuracy:", accuracy_score(y, rule_preds))
    print(classification_report(y, rule_preds, zero_division=0))

    agreement = sum(ml_preds == rule_preds)
    print(f"\nAgreement: {agreement}/{len(y)}")


if __name__ == "__main__":
    compare()
