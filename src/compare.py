import pandas as pd
from feature_engineering import create_ids_features
from model_utils import load_model
from rule_based import rule_predict
from sklearn.metrics import classification_report, accuracy_score

def compare():
    df = pd.read_csv("../data/processed_data.csv")

    X, y = create_ids_features(df)

    model = load_model()

    ml_preds = model.predict(X)
    rule_preds = rule_predict(X)

    print("\n=== ML Model Results ===")
    print("Accuracy:", accuracy_score(y, ml_preds))
    print(classification_report(y, ml_preds, zero_division=0))

    print("\n=== Rule-based Results ===")
    print("Accuracy:", accuracy_score(y, rule_preds))
    print(classification_report(y, rule_preds, zero_division=0))

    agreement = sum(ml_preds == rule_preds)
    print(f"\nAgreement: {agreement}/{len(y)}")

if __name__ == "__main__":
    compare()
