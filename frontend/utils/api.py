import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv(
    "AEGISAI_API_URL",
    "http://127.0.0.1:8000"
)

API_KEY = os.getenv(
    "AEGISAI_API_KEY",
    ""
)

headers = {
    "X-API-Key": API_KEY
}

# ==========================================
# HEALTH CHECK
# ==========================================

def check_health():

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=3
        )

        return (
            response.status_code == 200
        )

    except Exception:

        return False

# ==========================================
# PREDICTION
# ==========================================

def predict(data: dict):

    try:

        response = requests.post(

            f"{API_URL}/predict",

            json=data,

            headers=headers,

            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:

        return {
            "error": "Backend offline"
        }

    except requests.exceptions.Timeout:

        return {
            "error": "Backend timeout"
        }

    except Exception as e:

        return {
            "error": str(e)
        }