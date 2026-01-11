import pandas as pd
from sklearn.linear_model import LogisticRegression

def load_data():
    data = pd.read_csv("../data/processed_data.csv")
    X = data.drop("label", axis=1)
    y = data["label"]
    return X, y

def train_model(X, y):
    # Safety check
    if y.nunique() < 2:
        raise ValueError(
            "Training requires at least 2 classes. "
            "Current dataset has only one class."
        )

    model = LogisticRegression()
    model.fit(X, y)

    print("✅ Model trained successfully (using full dataset)")
    return model

if __name__ == "__main__":
    X, y = load_data()
    model = train_model(X, y)
