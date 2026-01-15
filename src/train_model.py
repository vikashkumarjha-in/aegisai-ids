from sklearn.linear_model import LogisticRegression
from feature_engineering import load_clean_data, split_features_labels, scale_features
from model_utils import save_model


def train_model():
    print("Loading dataset...")
    df = load_clean_data()

    X, y = split_features_labels(df)

    if y.nunique() < 2:
        raise ValueError("Dataset must contain at least two classes")

    print("Scaling features...")
    X_scaled = scale_features(X)

    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_scaled, y)

    print("Model training completed")
    save_model(model)


if __name__ == "__main__":
    train_model()
    print("Training completed successfully")
