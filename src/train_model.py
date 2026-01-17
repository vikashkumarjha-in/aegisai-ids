import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib
import os

DATA_PATH = "../data/processed_data.csv"
MODEL_PATH = "../models/ids_model.pkl"


def load_data():
    print("Loading processed dataset...")
    df = pd.read_csv(DATA_PATH)
    print("Dataset loaded successfully")

    X = df.drop("label", axis=1)
    y = df["label"]

    return X, y


def train_model(X, y):
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("Training Logistic Regression model...")
    model = LogisticRegression()
    model.fit(X_scaled, y)

    os.makedirs("../models", exist_ok=True)
    joblib.dump((model, scaler), MODEL_PATH)

    print("Model saved successfully")
    return model, scaler


if __name__ == "__main__":
    X, y = load_data()
    train_model(X, y)
    print("Training pipeline completed")
