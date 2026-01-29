import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import os

os.makedirs("../models", exist_ok=True)

X = np.random.rand(20, 5)
y = np.random.randint(0, 2, 20)

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "../models/latest_model.pkl")
print("[OK] Dummy model created successfully")
