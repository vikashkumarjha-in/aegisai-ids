import pandas as pd

def rule_predict(df: pd.DataFrame):
    predictions = []

    for _, row in df.iterrows():

        # Simple IDS rules using real NSL-KDD features
        if (
            row["src_bytes"] > 3000
            or row["count"] > 200
            or row["dst_host_srv_count"] > 200
        ):
            predictions.append(1)  # Attack
        else:
            predictions.append(0)  # Normal

    return predictions