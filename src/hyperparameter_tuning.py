# src/hyperparameter_tuning.py
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from feature_engineering import create_ids_features
from model_registry import save_model_version

DATA_PATH = "../data/processed_data.csv"

def load_features():
    df = pd.read_csv(DATA_PATH)
    X, y = create_ids_features(df)
    return X, y

def can_run_cv(y):
    # Must have at least 2 samples per class for CV; choose cv based on min class count
    counts = y.value_counts()
    if counts.min() < 2:
        return False, 0
    # choose cv to be at most min class count and not larger than 5
    cv = int(min(5, counts.min()))
    if cv < 2:
        return False, 0
    return True, cv

def tune_or_train(notes=""):
    X, y = load_features()
    n_samples = len(y)
    print(f"Loaded features: {X.shape}, samples: {n_samples}")
    possible, cv = can_run_cv(y)

    # define pipeline
    base_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2000, solver="liblinear"))
    ])

    if possible and n_samples >= 10:
        print(f"Running GridSearchCV with cv={cv}")
        param_grid = {
            "clf__C": [0.01, 0.1, 1, 10, 100],
            # solver 'liblinear' supports l1/l2; keep penalty l2 default for stability
        }
        cv_split = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
        grid = GridSearchCV(base_pipeline, param_grid, scoring="f1", cv=cv_split, n_jobs=-1, verbose=1)
        grid.fit(X, y)

        best = grid.best_estimator_
        best_score = float(grid.best_score_)
        print("Grid search complete. Best CV score (f1):", best_score)
        version, vpath, latest = save_model_version(best, metrics={"cv_f1": best_score}, notes=notes or "GridSearch tuning")
        print(f"Saved tuned model version {version} -> {vpath}")
        return version, best_score
    else:
        # Fallback: train a default model and save (safe when data is small)
        print("Dataset too small for reliable cross-validation tuning.")
        print("Training default pipeline (no grid search) and saving as a version.")
        base_pipeline.fit(X, y)
        # compute simple training accuracy for metadata
        y_pred = base_pipeline.predict(X)
        try:
            from sklearn.metrics import accuracy_score
            train_acc = float(accuracy_score(y, y_pred))
        except Exception:
            train_acc = None

        version, vpath, latest = save_model_version(base_pipeline, metrics={"train_accuracy": train_acc}, notes=notes or "Fallback train (no tuning)")
        print(f"Saved fallback model version {version} -> {vpath}")
        return version, train_acc

if __name__ == "__main__":
    tune_or_train(notes="Day 20 hyperparameter tuning run")
