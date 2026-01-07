import pandas as pd
import os

# Build absolute path safely
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "data", "sample.csv")

def test_load_dataset():
    print("Looking for dataset at:")
    print(DATASET_PATH)

    if not os.path.exists(DATASET_PATH):
        print("ERROR: Dataset file not found")
        return

    data = pd.read_csv(DATASET_PATH)
    print("Dataset loaded successfully")
    print("Shape:", data.shape)
    print(data.head())

if __name__ == "__main__":
    test_load_dataset()
