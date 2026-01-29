import joblib
import numpy as np

MODEL_PATH = "../models/latest_model.pkl"

print("[INFO] Loading IDS model...")
model = joblib.load(MODEL_PATH)

sample = np.random.rand(1, 5)
prediction = model.predict(sample)

print("[RESULT] Traffic classified as:", "ATTACK" if prediction[0] == 1 else "NORMAL")
