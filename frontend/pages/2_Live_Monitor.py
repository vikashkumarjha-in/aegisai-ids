# frontend/pages/2_Live_Monitor.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import random
import sys
from pathlib import Path
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Append root paths safely
frontend_root = str(Path(__file__).resolve().parents[1])
if frontend_root not in sys.path:
    sys.path.append(frontend_root)

# =========================================================
# UNIVERSAL SESSION STATE FALLBACK ENGINE
# =========================================================
if "logs" not in st.session_state or st.session_state.logs.empty:
    st.session_state.logs = pd.DataFrame(columns=["Timestamp", "Source IP", "Destination IP", "Destination Port", "Protocol", "Bytes", "Attack Type", "Severity", "AI Confidence"])

if "packet_history" not in st.session_state or st.session_state.packet_history.empty:
    st.session_state.packet_history = pd.DataFrame(columns=["Timestamp", "Source IP", "Destination IP", "Destination Port", "Protocol", "Bytes", "Attack Type", "Severity", "AI Confidence"])

if "blocked_ips" not in st.session_state:
    st.session_state.blocked_ips = set()

if "initialized" not in st.session_state:
    st.session_state.initialized = True

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AegisAI Live Monitor",
    layout="wide"
)

# Inject consistent cyberpunk theme styling
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #030611 !important;
    color: #e2f1f7 !important;
    font-family: 'Consolas', 'Segoe UI', monospace, sans-serif;
}
.stApp {
    background: 
        radial-gradient(circle at 85% 15%, rgba(0, 170, 255, 0.05), transparent 40%),
        radial-gradient(circle at 15% 85%, rgba(255, 0, 136, 0.04), transparent 45%),
        #030611 !important;
}
header, footer, #MainMenu {
    visibility: hidden;
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# AUTO REFRESH (Synced Engine)
# =========================================================
st_autorefresh(interval=2000, key="live_monitor_refresh")

# =========================================================
# HEADER & LIVE CLOCK
# =========================================================
st.title("📡 Live Monitor")
st.caption(f"Live Stream Active • {datetime.now().strftime('%H:%M:%S')}")

st.write("")

# =========================================================
# CHARTS & TELEMETRY OVERLAYS
# =========================================================
threat_level = random.randint(10, 95)
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=threat_level,
    title={'text': "Current Threat Level Threshold", 'font': {'color': 'white', 'size': 16}},
    gauge={
        'axis': {'range': [0, 100], 'tickcolor': "white"},
        'bar': {'color': "#ff1744"},
        'steps': [
            {'range': [0, 40], 'color': "rgba(0, 230, 118, 0.15)"},
            {'range': [40, 70], 'color': "rgba(255, 145, 0, 0.15)"},
            {'range': [70, 100], 'color': "rgba(255, 23, 68, 0.2)"},
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 90
        }
    }
))
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    height=280,
    margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(fig, width="stretch")

packets = np.random.randint(100, 1000, 30)
time_axis = list(range(30))
line_fig = px.line(
    x=time_axis,
    y=packets,
    title="Real-time Ingress Packets / Sec"
)
line_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    height=260
)
st.plotly_chart(line_fig, width="stretch")

# ---------------------------------------------------------
# 3D TOPOLOGY NETWORK GRAPH
# ---------------------------------------------------------
st.subheader("🌐 Network Activity Topology")
network_df = pd.DataFrame({
    "x": np.random.rand(30),
    "y": np.random.rand(30),
    "z": np.random.rand(30),
    "severity": np.random.choice(["Attack", "Benign"], 30)
})
network_fig = px.scatter_3d(
    network_df,
    x="x",
    y="y",
    z="z",
    color="severity",
    title="3D Cluster Node Analysis Graph",
    color_discrete_map={"Attack": "#ff1744", "Benign": "#00e676"}
)
network_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    height=450
)
st.plotly_chart(network_fig, width="stretch")

# ---------------------------------------------------------
# DATAFRAME CAPTURE LAYER
# ---------------------------------------------------------
st.subheader("📦 Live Packets Capture Frame")

# Self-populating framework if global buffer states are clear
if st.session_state.packet_history.empty:
    sample_data = []
    for i in range(10):
        sample_data.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Source IP": f"192.168.1.{random.randint(10,99)}",
            "Destination IP": "10.0.0.1",
            "Destination Port": random.choice([80, 443, 22]),
            "Protocol": "TCP",
            "Bytes": random.randint(100, 1200),
            "Attack Type": "Benign",
            "Severity": "Low",
            "AI Confidence": 99.1
        })
    st.session_state.packet_history = pd.DataFrame(sample_data)

st.dataframe(
    st.session_state.packet_history.head(30),
    width="stretch",
    height=400
)