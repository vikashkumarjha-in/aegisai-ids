import pandas as pd

def load_dataset(path):
    data = pd.read_csv(path)
    print("Dataset loaded successfully")
    print("Shape:", data.shape)
    return data

if __name__ == "__main__":
    dataset_path = "../data/sample.csv"
    load_dataset(dataset_path)
