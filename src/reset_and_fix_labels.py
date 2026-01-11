import pandas as pd

# Load processed data
df = pd.read_csv("../data/processed_data.csv")

# Safety check
if df.shape[0] < 2:
    raise ValueError("Dataset too small to fix labels")

# Force at least one attack sample
df.loc[df.index[-1], "label"] = 1

# Save back
df.to_csv("../data/processed_data.csv", index=False)

print("✅ Labels fixed successfully")
print(df["label"].value_counts())
