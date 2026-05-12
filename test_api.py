import requests

url = "https://aegisai-ids.onrender.com/predict"

data = {
    "duration": 0,
    "protocol_type": "tcp",
    "src_bytes": 100,
    "dst_bytes": 50,
    "count": 10
}

try:
    res = requests.post(url, json=data, timeout=10)
    print("STATUS:", res.status_code)
    print("RESPONSE:", res.json())
except Exception as e:
    print("ERROR:", e)