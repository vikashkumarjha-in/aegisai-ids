# src/cicids_plan.py
import json, os

PLAN = {
  "source": "CICIDS2017 (metadata only; files not downloaded)",
  "expected_columns": [
    "Tot Fwd Pkts",
    "Tot Backward Pkts",
    "Flow Duration",
    "Label"
  ],
  "feature_mapping": {
    "packet_ratio": "Tot Fwd Pkts / (Tot Backward Pkts + 1)",
    "high_activity": "Flow Duration > median(Flow Duration)"
  },
  "label_mapping": {
    "BENIGN": "normal"
    # all other labels -> "attack"
  },
  "notes": "Run ingestion when dataset is available. For Day 23 testing we generate a synthetic sample."
}

OUT = os.path.join("data", "cicids_plan.json")
os.makedirs("data", exist_ok=True)
with open(OUT, "w") as f:
    json.dump(PLAN, f, indent=2)
print("Saved processing plan to", OUT)
