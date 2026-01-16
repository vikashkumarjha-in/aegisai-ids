import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from feature_engineering import scale_features
from model_utils import save_model

DATA_PATH = "../data/processed_data.csv"


def load_data():
    print("Loading processed dataset...")
    data = pd.read_csv(DATA_PATH)

    if "label" not in data.columns:
        raise ValueError("'label' column not found in dataset")

    X = data.drop("label", axis=1)
    y = data["label"]

    if y.nunique() < 2:
        raise ValueError("Dataset must contain at least two classes")

    return X, y


def train_model(X, y):
    print("Attempting train-test split...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ✅ CRITICAL SAFETY CHECK
    if y_train.nunique() < 2:
        print(
            "⚠️ Warning: Training split has only one class. "
            "Falling back to training on full dataset."
        )
        X_train = X
        y_train = y
        X_test = X
        y_test = y

    print("Scaling training features...")
    X_train_scaled = scale_features(X_train)

    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    print("Model training completed")
    return model, X_test, y_test


if __name__ == "__main__":
    X, y = load_data()
    model, X_test, y_test = train_model(X, y)
    save_model(model)

    print("Training phase completed successfully.")
