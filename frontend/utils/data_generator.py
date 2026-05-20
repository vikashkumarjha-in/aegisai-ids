import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
ATTACK_TYPES = [
"DDoS",
"Port Scan",
"Brute Force",
"Web Attack",
"Botnet",
"Infiltration",
"Benign"
]
SEVERITY_MAP = {
"DDoS": "Critical",
"Port Scan": "Medium",
"Brute Force": "High",
"Web Attack": "High",
"Botnet": "Critical",
"Infiltration": "Critical",
"Benign": "Low"
}
COUNTRIES = [
"USA",
"India",
"Germany",
"China",
"Russia",
"Brazil",
"France",
"UK"
]
PROTOCOLS = ["TCP", "UDP", "ICMP"]
def random_ip():
return ".".join(str(random.randint(1, 255)) for _ in range(4))
def generate_event():

attack = random.choices(
ATTACK_TYPES,
weights=[15, 12, 10, 8, 5, 3, 47]
)[0]
return {
"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
"Source IP": random_ip(),
"Destination IP": random_ip(),
"Dest Port": random.choice([21, 22, 53, 80, 443, 8080]),
"Protocol": random.choice(PROTOCOLS),
"Bytes": random.randint(40, 15000),
"Packets": random.randint(1, 400),
"Attack Type": attack,
"Severity": SEVERITY_MAP[attack],
"Action": random.choice(["Blocked", "Allowed", "Monitored"]),
"Country": random.choice(COUNTRIES),
"Prediction": attack
}
def generate_logs(n=100):
return pd.DataFrame([generate_event() for _ in range(n)])
def generate_alert_trend():
hours = pd.date_range(end=datetime.now(), periods=24, freq="H")
alerts = np.random.randint(20, 150, size=24)
alerts[5] = 220
alerts[13] = 300
alerts[19] = 260
return pd.DataFrame({
"Hour": hours,
"Alerts": alerts
})
def generate_attack_timeline():
dates = pd.date_range(end=datetime.now(), periods=7)
return pd.DataFrame({
"Date": dates,
"DDoS": np.random.randint(50, 200, 7),
"Port Scan": np.random.randint(30, 150, 7),
"Brute Force": np.random.randint(20, 100, 7)
})

def generate_heatmap_data():
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
hours = list(range(24))
data = []
for d in days:
for h in hours:
data.append([
d,
h,
random.randint(0, 120)
])
return pd.DataFrame(data, columns=["Day", "Hour", "Count"])
 
