import streamlit as st
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

st.title("Security Logs")

st_autorefresh(interval=3000, key="logs_refresh")

if "logs" not in st.session_state:

    st.session_state.logs = pd.DataFrame({
        "Timestamp": pd.date_range(
            "2026-01-01",
            periods=100,
            freq="min"
        ),
        "Source IP": [
            f"192.168.1.{i%50}"
            for i in range(100)
        ],
        "Dest Port": np.random.randint(
            20,
            9000,
            100
        ),
        "Protocol": np.random.choice(
            ["TCP", "UDP", "ICMP"],
            100
        ),
        "Bytes": np.random.randint(
            100,
            5000,
            100
        ),
        "Attack Type": np.random.choice(
            [
                "Benign",
                "DDoS",
                "Port Scan",
                "Botnet"
            ],
            100
        ),
        "Severity": np.random.choice(
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ],
            100
        )
    })

logs = st.session_state.logs

severity_filter = st.selectbox(
    "Severity",
    ["All", "Low", "Medium", "High", "Critical"]
)

filtered = logs.copy()

if severity_filter != "All":

    filtered = filtered[
        filtered["Severity"] == severity_filter
    ]

search = st.text_input("Search IP")

if search:

    filtered = filtered[
        filtered["Source IP"].str.contains(search)
    ]

st.dataframe(
    filtered,
    use_container_width=True
)