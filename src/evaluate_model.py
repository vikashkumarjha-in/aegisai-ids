# src/evaluate_model.py
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
from feature_engineering import create_ids_features
from model_utils import load_model

DATA_PATH = "../data/processed_data.csv"

def evaluate_model():
    print("Loading model...")
    model = load_model()

    print("Loading evaluation dataset...")
    df = pd.read_csv(DATA_PATH)

    print("Creating IDS-based features...")
    X, y = create_ids_features(df)

    print("Running predictions...")
    y_pred = model.predict(X)

    print("\nAccuracy:", accuracy_score(y, y_pred))
    print("\nClassification Report:")
    print(classification_report(y, y_pred))

if __name__ == "__main__":
    evaluate_model()
