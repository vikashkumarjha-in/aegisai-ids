import pandas as pd

def create_ids_features(df: pd.DataFrame):
    df = df.copy()

    feature_cols = [c for c in df.columns if c != "label"]

    X = df[feature_cols]

    y = df["label"] if "label" in df.columns else None

    return X, y