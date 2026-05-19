import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COLUMNS = [
    "duration","protocol_type","service","flag",
    "src_bytes","dst_bytes","land","wrong_fragment",
    "urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted",
    "num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login",
    "is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate",
    "same_srv_rate","diff_srv_rate","srv_diff_host_rate",
    "dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate",
    "dst_host_srv_rerror_rate","label","difficulty_level"
]

def preprocess(path_in, path_out):
    df = pd.read_csv(path_in, header=None, names=COLUMNS)

    df = df.drop(columns=["difficulty_level"])

    # Convert labels
    df["label"] = (df["label"] != "normal").astype(int)

    # Encode text columns
    for col in ["protocol_type", "service", "flag"]:
        df[col] = LabelEncoder().fit_transform(df[col])

    # Remove duplicates
    df = df.drop_duplicates()

    # Save processed dataset
    df.to_csv(path_out, index=False)

    print(f"Saved {len(df)} rows")
    print("Dataset preprocessing completed")

if __name__ == "__main__":
    preprocess(
        os.path.join(BASE_DIR, "data", "nslkdd", "KDDTrain+.txt"),
        os.path.join(BASE_DIR, "data", "processed_nslkdd.csv")
    )