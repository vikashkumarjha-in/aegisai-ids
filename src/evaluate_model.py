import pandas as pd
import joblib
from sklearn.metrics import classification_report, accuracy_score

DATA_PATH = "../data/processed_data.csv"
MODEL_PATH = "../models/ids_model.pkl"


def evaluate_model():
    print("Loading model and scaler...")
    model, scaler = joblib.load(MODEL_PATH)

    print("Loading evaluation dataset...")
    df = pd.read_csv(DATA_PATH)

    X = df.drop("label", axis=1)
    y = df["label"]

    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)

    print("\nEvaluation Results:")
    print("Accuracy:", accuracy_score(y, y_pred))
    print("\nClassification Report:")
    print(classification_report(y, y_pred))


if __name__ == "__main__":
    evaluate_model()
