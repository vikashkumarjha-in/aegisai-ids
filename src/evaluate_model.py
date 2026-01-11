import pandas as pd
from sklearn.metrics import classification_report
from train_model import train_model

def load_data():
    data = pd.read_csv("../data/processed_data.csv")
    X = data.drop("label", axis=1)
    y = data["label"]
    return X, y

if __name__ == "__main__":
    X, y = load_data()
    model = train_model(X, y)

    predictions = model.predict(X)

    print("\n📊 Model Evaluation (Prototype)")
    print(classification_report(y, predictions))
