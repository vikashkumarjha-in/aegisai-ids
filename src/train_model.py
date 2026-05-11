# src/train_model.py
from feature_engineering import create_ids_features


import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.utils import resample
from feature_engineering import create_ids_features
from model_registry import save_model_version
from sklearn.metrics import accuracy_score

DATA_PATH = "../data/processed_data.csv"

def load_raw_data():
    print("Loading processed dataset...")
    df = pd.read_csv(DATA_PATH)
    print("Dataset loaded:", df.shape)
    return df

def balance_data_if_needed(X, y, threshold_ratio=1.5):
    counts = y.value_counts()
    if len(counts) < 2:
        raise ValueError("Need at least two classes to train.")
    maj = counts.idxmax()
    minc = counts.idxmin()
    maj_count = counts.max()
    min_count = counts.min()

    ratio = maj_count / float(min_count)
    print(f"Class counts before balancing:\n{counts.to_dict()}  (ratio={ratio:.2f})")

    if ratio < threshold_ratio:
        print("Classes reasonably balanced — no oversampling.")
        return X, y, False

    if len(y) <= 200:
        print("Small dataset and imbalance detected — performing random oversampling of minority class.")
        df_xy = X.copy()
        df_xy["label"] = y.values

        majority = df_xy[df_xy["label"] == maj]
        minority = df_xy[df_xy["label"] == minc]

        minority_upsampled = resample(minority,
                                      replace=True,
                                      n_samples=maj_count,
                                      random_state=42)
        balanced = pd.concat([majority, minority_upsampled])
        balanced = balanced.sample(frac=1, random_state=42).reset_index(drop=True)
        X_bal = balanced.drop(columns=["label"])
        y_bal = balanced["label"]
        print("Class counts after oversampling:", y_bal.value_counts().to_dict())
        return X_bal, y_bal, True

    print("Large dataset — using class_weight in model.")
    return X, y, False

def train_model_and_version(notes: str = ""):
    df = load_raw_data()
    X, y = create_ids_features(df)

    X_bal, y_bal, did_oversample = balance_data_if_needed(X, y)

    if did_oversample:
        clf = LogisticRegression(max_iter=1000)
    else:
        clf = LogisticRegression(class_weight="balanced", max_iter=1000)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", clf)
    ])

    print("Training model on features:", list(X_bal.columns))
    pipeline.fit(X_bal, y_bal)

    # compute training accuracy for metadata
    y_pred = pipeline.predict(X_bal)
    train_acc = float(accuracy_score(y_bal, y_pred))

    # save versioned model and write experiments.csv
    metrics = {"train_accuracy": train_acc}
    version, version_path, latest_path = save_model_version(pipeline, metrics=metrics, notes=notes)

    print(f"Model saved: version={version}, path={version_path}")
    print("Latest model also updated at:", latest_path)
    return version

if __name__ == "__main__":
    v = train_model_and_version(notes="Day 19 training")
    print("Training + versioning completed. Version:", v)
