# src/feature_engineering.py
import pandas as pd

def create_ids_features(df: pd.DataFrame):
    """
    Converts input dataframe into model-ready features.
    """
    df = df.copy()

    df["packet_ratio"] = df["src_bytes"] / (df["dst_bytes"] + 1)
    df["high_activity"] = (df["count"] > 100).astype(int)

    X = df[["packet_ratio", "high_activity"]]
    y = df["label"] if "label" in df.columns else None

    return X, y
