# src/model_registry.py
import os
import joblib
import pandas as pd
from datetime import datetime

MODELS_DIR = "../models"
LATEST_PATH = os.path.join(MODELS_DIR, "ids_model.pkl")
EXPERIMENTS_CSV = os.path.join(MODELS_DIR, "experiments.csv")
VERSION_PREFIX = "ids_model_v"

def _ensure_models_dir():
    os.makedirs(MODELS_DIR, exist_ok=True)

def get_next_version():
    _ensure_models_dir()
    files = [f for f in os.listdir(MODELS_DIR) if f.startswith(VERSION_PREFIX) and f.endswith(".pkl")]
    versions = []
    for f in files:
        try:
            v = int(f.replace(VERSION_PREFIX, "").replace(".pkl", ""))
            versions.append(v)
        except:
            continue
    return max(versions) + 1 if versions else 1

def save_model_version(obj, metrics: dict = None, notes: str = ""):
    """
    Save a pipeline (or any object) as a new version, record metrics in experiments.csv,
    and update the 'latest' model path.
    - obj: pipeline or model object to save via joblib
    - metrics: dict of numeric metrics (e.g. {'train_accuracy':0.9})
    - notes: short text
    Returns the version number and paths.
    """
    _ensure_models_dir()
    version = get_next_version()
    filename = f"{VERSION_PREFIX}{version}.pkl"
    version_path = os.path.join(MODELS_DIR, filename)

    # save versioned model
    joblib.dump(obj, version_path)

    # also save/overwrite the 'latest' model for legacy scripts
    joblib.dump(obj, LATEST_PATH)

    # append experiment metadata
    row = {
        "version": version,
        "filename": filename,
        "saved_at": datetime.utcnow().isoformat(),
        "notes": notes
    }
    if metrics:
        for k, v in metrics.items():
            row[k] = v

    # ensure CSV exists and append row
    if not os.path.exists(EXPERIMENTS_CSV):
        df = pd.DataFrame([row])
        df.to_csv(EXPERIMENTS_CSV, index=False)
    else:
        df = pd.DataFrame([row])
        df.to_csv(EXPERIMENTS_CSV, mode="a", header=False, index=False)

    return version, version_path, LATEST_PATH
