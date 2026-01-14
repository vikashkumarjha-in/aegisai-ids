import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from model_utils import load_model

DATA_PATH = "../data/processed_data.csv"

def load_data():
    print("Loading dataset for evaluation...")
    data = pd.read_csv(DATA_PATH)

    if "label" not in data.columns:
        raise ValueError("'label' column not found in dataset")

    X = data.drop("label", axis=1)
    y = data["label"]

    return X, y

def evaluate_model(model, X, y):
    print("Evaluating model...")
    predictions = model.predict(X)

    accuracy = accuracy_score(y, predictions)
    print(f"Model Accuracy: {accuracy:.4f}\n")

    print("Classification Report:")
    print(classification_report(y, predictions))

if __name__ == "__main__":
    X, y = load_data()
    model = load_model()   # ← THIS IS WHERE IT IS USED CORRECTLY
    evaluate_model(model, X, y)

    print("Evaluation completed successfully.")
