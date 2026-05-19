import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "processed_nslkdd.csv")

MODEL_PATH = os.path.join(BASE_DIR, "models", "latest_model.pkl")


def train_model():

    print("Loading processed dataset...")

    df = pd.read_csv(DATA_PATH)

    print(f"Dataset loaded: {df.shape}")

    # Features and labels
    X = df.drop(columns=["label"])

    y = df["label"]

    print(f"Training on {X.shape[1]} features")

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    # Train
    print("Training RandomForest model...")

    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("\n=== MODEL RESULTS ===")

    print(f"Accuracy: {accuracy:.4f}")

    print(classification_report(y_test, y_pred))

    # Save model
    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved to:\n{MODEL_PATH}")


if __name__ == "__main__":
    train_model()