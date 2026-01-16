from sklearn.metrics import accuracy_score, classification_report
from feature_engineering import scale_features
from model_utils import load_model
from train_model import load_data, train_model


def evaluate_model():
    print("Preparing evaluation data...")
    X, y = load_data()

    model, X_test, y_test = train_model(X, y)

    print("Scaling test features...")
    X_test_scaled = scale_features(X_test)

    print("Loading trained model...")
    model = load_model()

    print("Evaluating model...")
    predictions = model.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, predictions)
    print(f"\nModel Accuracy: {accuracy:.4f}\n")

    print("Classification Report:")
    print(classification_report(y_test, predictions))


if __name__ == "__main__":
    evaluate_model()
