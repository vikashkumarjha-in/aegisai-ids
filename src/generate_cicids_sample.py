# src/generate_cicids_sample.py
import pandas as pd
import numpy as np
import os

OUT = os.path.join("data", "processed_data.csv")  # this is what your pipeline expects
n = 200

# Simulated raw CICIDS columns (integer counts; flow duration in ms)
np.random.seed(42)
tot_fwd = np.random.poisson(10, size=n) + 1
tot_back = np.random.poisson(8, size=n)
flow_dur = np.random.exponential(scale=200, size=n).astype(int) + 1

# Labels: create a mix: ~80% normal, 20% attacks
labels = np.where(np.random.rand(n) < 0.8, "BENIGN", "DoS")

# Build DataFrame with the real header names used by CICIDS ingestion script
df = pd.DataFrame({
    "Tot Fwd Pkts": tot_fwd,
    "Tot Backward Pkts": tot_back,
    "Flow Duration": flow_dur,
    "Label": labels
})

# Now transform to our simplified processed_data.csv schema:
df["packet_ratio"] = df["Tot Fwd Pkts"] / (df["Tot Backward Pkts"] + 1)
median_duration = df["Flow Duration"].median()
df["high_activity"] = (df["Flow Duration"] > median_duration).astype(int)
df["label"] = df["Label"].apply(lambda x: "normal" if str(x).upper()=="BENIGN" else "attack")

out = df[["packet_ratio", "high_activity", "label"]]
os.makedirs("data", exist_ok=True)
out.to_csv(OUT, index=False)
print("Synthetic sample saved to", OUT)
print(out.head())
