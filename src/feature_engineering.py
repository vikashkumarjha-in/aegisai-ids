import pandas as pd
import numpy as np
import os


def load_clean_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "sample.csv")

    if not os.path.exists(data_path):
        print("ERROR: Dataset not found")
        return None

    df = pd.read_csv(data_path)
    return df


def split_features_labels(df):
    X = df.drop(columns=["label"])
    y = df["label"]
    print("Features and labels separated")
    return X, y


def normalize_features(X):
    X_norm = (X - X.mean()) / X.std()
    print("Features normalized")
    return X_norm


if __name__ == "__main__":
    df = load_clean_data()

    if df is not None:
        X, y = split_features_labels(df)
        X = normalize_features(X)

        print("\nFeature Engineering Complete")
        print("Feature sample:")
        print(X.head())
        print("Label sample:")
        print(y.head())
