import streamlit as st
import pandas as pd

st.title("📜 Security Logs")

logs = pd.DataFrame({
    "IP": ["192.168.1.1", "10.0.0.5"],
    "Threat": ["DDoS", "SQL Injection"],
    "Severity": ["High", "Critical"]
})

st.dataframe(logs)