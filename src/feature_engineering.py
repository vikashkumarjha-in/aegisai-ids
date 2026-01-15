import pandas as pd
import os
from sklearn.preprocessing import StandardScaler


def load_clean_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "processed_data.csv")

    if not os.path.exists(data_path):
        raise FileNotFoundError("Processed dataset not found")

    df = pd.read_csv(data_path)
    return df


def split_features_labels(df):
    if "label" not in df.columns:
        raise ValueError("'label' column not found in dataset")

    X = df.drop(columns=["label"])
    y = df["label"]

    print("Features and labels separated")
    return X, y


def scale_features(X):
    """
    Standardize features using StandardScaler
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("Features scaled using StandardScaler")
    return X_scaled
