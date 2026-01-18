import pandas as pd


def load_data(path):
    print("Loading raw data...")
    df = pd.read_csv(path)
    return df


def create_ids_features(df):
    """
    Convert raw features into IDS-style behavioral features
    """

    print("Creating IDS-based features...")

    # Example behavioral features
    df["packet_ratio"] = df["feature1"] / (df["feature2"] + 1)
    df["high_activity"] = (df["feature1"] > 20).astype(int)

    X = df[["packet_ratio", "high_activity"]]
    y = df["label"]

    return X, y


if __name__ == "__main__":
    df = load_data("../data/processed_data.csv")
    X, y = create_ids_features(df)

    print("\nFeature Engineering Output:")
    print(X.head())
    print("\nLabels:")
    print(y.head())
