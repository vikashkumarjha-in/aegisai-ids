# src/preprocess.py

import os
import pandas as pd
import numpy as np

# ===============================
# PATH CONFIGURATION
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sample.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed_data.csv")


def load_data():
    if not os.path.exists(DATA_PATH):
        print("ERROR: Dataset not found")
        return None

    df = pd.read_csv(DATA_PATH)
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

        # Save processed dataset
        df.to_csv(OUTPUT_PATH, index=False)
        print(f"Processed data saved as {OUTPUT_PATH}")
