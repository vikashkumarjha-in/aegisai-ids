import streamlit as st
import pandas as pd
from utils.data_generator import generate_logs
from utils.styles import load_css
st.set_page_config(
page_title="AegisAI SOC",
layout="wide",
initial_sidebar_state="expanded"
)
load_css()
if "initialized" not in st.session_state:
st.session_state.initialized = True
logs = generate_logs(120)
st.session_state.logs = logs
st.session_state.packet_history = logs.copy()
st.session_state.alerts = logs[
logs["Severity"].isin(["Critical", "High"])
].head(10)

st.title("🛡️ AegisAI Security Operations Center"
)
st.markdown(
"""
### Enterprise Intrusion Detection & Threat Intelligence Platform
Navigate using the sidebar.
"""
)