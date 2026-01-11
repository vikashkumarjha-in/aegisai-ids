import pandas as pd
import os

DATA_PATH = "../data/processed_data.csv"

df = pd.read_csv(DATA_PATH)

print("Before fix:")
print(df["label"].value_counts())

# Add dummy attack traffic (5% as attacks)
attack_count = int(0.05 * len(df))
df.loc[:attack_count, "label"] = 1

df.to_csv(DATA_PATH, index=False)

print("\nAfter fix:")
print(df["label"].value_counts())
print("\n✅ Labels fixed successfully")
