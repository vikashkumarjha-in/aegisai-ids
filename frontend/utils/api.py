import requests

API_URL = "https://aegisai-ids.onrender.com/predict"

def predict(data):
    try:
        response = requests.post(API_URL, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}