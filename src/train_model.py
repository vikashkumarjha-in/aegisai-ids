import pandas as pd
from sklearn.linear_model import LogisticRegression

def load_data():
    data = pd.read_csv("processed_data.csv")
    X = data.drop("label", axis=1)
    y = data["label"]
    return X, y

def train_model(X, y):
    model = LogisticRegression()
    model.fit(X, y)   # Direct training (NO SPLIT)
    return model

if __name__ == "__main__":
    X, y = load_data()
    model = train_model(X, y)
    print("Model trained successfully!")
