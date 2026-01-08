import pandas as pd
import numpy as np
import os


def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "sample.csv")

    if not os.path.exists(data_path):
        print("ERROR: Dataset not found")
        return None

    df = pd.read_csv(data_path)
    print("Dataset loaded")
    print("Shape:", df.shape)
    return df


def check_missing_values(df):
    print("\nMissing values per column:")
    print(df.isnull().sum())


def remove_duplicates(df):
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    print(f"\nDuplicates removed: {before - after}")
    return df


def encode_labels(df):
    if "label" not in df.columns:
        print("No label column found")
        return df

    df["label"] = df["label"].map({
        "normal": 0,
        "attack": 1
    })
    print("\nLabels encoded (normal=0, attack=1)")
    return df


if __name__ == "__main__":
    df = load_data()

    if df is not None:
        check_missing_values(df)
        df = remove_duplicates(df)
        df = encode_labels(df)

        print("\nPreprocessing complete")
        print(df.head())
