# src/rule_based.py
import pandas as pd
from feature_engineering import create_ids_features

def rule_predict(X):
    """
    Simple rule-based detector using IDS-style features.
    Returns a list/array of 0/1 predictions.
    Rules here are illustrative — tweak later.
    """
    preds = []
    for _, row in X.iterrows():
        # Example rules:
        # - If packet_ratio is high -> suspicious
        # - Or if high_activity flag is set -> suspicious
        if row["packet_ratio"] > 1.5 or row["high_activity"] == 1:
            preds.append(1)
        else:
            preds.append(0)
    return preds

if __name__ == "__main__":
    df = pd.read_csv("../data/processed_data.csv")
    X, y = create_ids_features(df)
    preds = rule_predict(X)
    print("Rule-based predictions:", preds)
    print("True labels:", list(y))
