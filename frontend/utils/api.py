# frontend/utils/api.py

import requests
import os

# =========================================================
# API URL
# =========================================================

API_URL = os.getenv(
    "AEGISAI_API_URL",
    "http://127.0.0.1:8000"
)

# =========================================================
# HEALTH CHECK
# =========================================================

def check_health():

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=3
        )

        return response.status_code == 200

    except Exception:

        return False

# =========================================================
# PREDICT
# =========================================================

def predict(data=None):

    try:

        response = requests.get(
            f"{API_URL}/predict",
            timeout=5
        )

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }