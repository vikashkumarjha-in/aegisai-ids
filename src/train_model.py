import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from feature_engineering import create_ids_features
from model_utils import save_model

DATA_PATH = "../data/processed_data.csv"

def load_data():
    print("Loading processed dataset...")
    df = pd.read_csv(DATA_PATH)
    return df

def train_model():
    df = load_data()

    X, y = create_ids_features(df)

    print("Training ML model using IDS-based features...")

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X, y)

    save_model(pipeline)
    print("Model trained and saved successfully")

if __name__ == "__main__":
    train_model()
