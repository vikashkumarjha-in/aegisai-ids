import pandas as pd
from sklearn.linear_model import LogisticRegression
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
    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model

if __name__ == "__main__":
    X, y = load_data()
    model = train_model(X, y)
    save_model(model)

    print("Training completed successfully.")
