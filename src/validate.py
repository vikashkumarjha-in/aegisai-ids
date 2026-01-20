# src/validate.py
import os
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
)
from feature_engineering import create_ids_features

MODEL_PATH = "../models/ids_model.pkl"
DATA_PATH = "../data/processed_data.csv"
OUTPUT_IMAGE = "../models/confusion_matrix.png"


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Trained model not found. Run training first.")
    # model saved earlier is a pipeline (scaler + model) or tuple; handle both
    obj = joblib.load(MODEL_PATH)
    # if model saved as (model, scaler), detect and convert to pipeline-like predict
    if isinstance(obj, tuple) or isinstance(obj, list):
        model, scaler = obj
        class Wrapper:
            def __init__(self, model, scaler):
                self.model = model
                self.scaler = scaler

            def predict(self, X):
                Xs = self.scaler.transform(X)
                return self.model.predict(Xs)
        return Wrapper(model, scaler)
    return obj


def save_confusion_image(cm, labels, path):
    import matplotlib.pyplot as plt
    # create figure
    fig, ax = plt.subplots()
    ax.imshow(cm)
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    # annotate cells with numbers
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    # ensure folder exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


def evaluate_and_save():
    print("Loading model...")
    model = load_model()

    print("Loading data & creating features...")
    df = pd.read_csv(DATA_PATH)
    X, y = create_ids_features(df)

    print("Running predictions...")
    y_pred = model.predict(X)

    acc = accuracy_score(y, y_pred)
    print(f"\nAccuracy: {acc:.4f}\n")
    print("Classification Report:")
    print(classification_report(y, y_pred, zero_division=0))

    # confusion matrix
    labels = np.unique(y)
    cm = confusion_matrix(y, y_pred, labels=labels)
    save_confusion_image(cm, labels, OUTPUT_IMAGE)
    print(f"\nConfusion matrix saved to: {OUTPUT_IMAGE}")


if __name__ == "__main__":
    evaluate_and_save()
