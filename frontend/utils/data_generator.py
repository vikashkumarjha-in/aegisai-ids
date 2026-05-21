import random
import pandas as pd
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

PROTOCOLS = ["TCP", "UDP", "ICMP"]

COUNTRIES = [
    "United States",
    "China",
    "Russia",
    "India",
    "Germany",
    "Brazil",
    "United Kingdom",
    "Japan",
    "France",
    "Australia"
]

SEVERITIES = {
    "DDoS": "Critical",
    "Port Scan": "Medium",
    "Brute Force": "High",
    "Web Attack": "High",
    "Botnet": "Critical",
    "Infiltration": "Critical",
    "Benign": "Low"
}

def random_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))


def generate_event():
    attack = random.choice(ATTACK_TYPES)

    now = datetime.now()

    return {
        "Timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "Source IP": random_ip(),
        "Destination IP": random_ip(),
        "Dest Port": random.choice([21, 22, 53, 80, 443, 8080, 3306]),
        "Protocol": random.choice(PROTOCOLS),
        "Bytes": random.randint(400, 15000),
        "Packets": random.randint(4, 120),
        "Attack Type": attack,
        "Severity": SEVERITIES[attack],
        "Country": random.choice(COUNTRIES),
        "Action": random.choice([
            "Blocked",
            "Allowed",
            "Monitored",
            "Quarantined"
        ]),
        "AI Confidence": round(random.uniform(91.2, 99.9), 2)
    }


def generate_bulk_events(count=200):
    rows = []

    for i in range(count):
        attack = random.choice(ATTACK_TYPES)

        timestamp = datetime.now() - timedelta(
            seconds=random.randint(1, 7200)
        )

        rows.append({
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Source IP": random_ip(),
            "Destination IP": random_ip(),
            "Dest Port": random.choice([21, 22, 53, 80, 443, 8080, 3306]),
            "Protocol": random.choice(PROTOCOLS),
            "Bytes": random.randint(400, 15000),
            "Packets": random.randint(4, 120),
            "Attack Type": attack,
            "Severity": SEVERITIES[attack],
            "Country": random.choice(COUNTRIES),
            "Action": random.choice([
                "Blocked",
                "Allowed",
                "Monitored",
                "Quarantined"
            ]),
            "AI Confidence": round(random.uniform(91.2, 99.9), 2)
        })

    return pd.DataFrame(rows)