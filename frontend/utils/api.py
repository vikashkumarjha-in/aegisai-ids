import requests

API_URL = "http://127.0.0.1:8000"


def check_health():

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=3
        )

        return response.status_code == 200

    except Exception:

        return False


def predict(data):

    try:

        response = requests.post(
            f"{API_URL}/predict",
            json=data,
            timeout=5
        )

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }