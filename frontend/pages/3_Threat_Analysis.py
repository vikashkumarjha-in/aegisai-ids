# frontend/pages/3_Threat_Analysis.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Append utility paths safely
frontend_root = str(Path(__file__).resolve().parents[1])
if frontend_root not in sys.path:
    sys.path.append(frontend_root)

# =========================================================
# UNIVERSAL SESSION STATE FALLBACK ENGINE
# =========================================================
if "logs" not in st.session_state:
    st.session_state.logs = pd.DataFrame()

if "packet_history" not in st.session_state:
    st.session_state.packet_history = pd.DataFrame()

if "blocked_ips" not in st.session_state:
    st.session_state.blocked_ips = set()

if "initialized" not in st.session_state:
    st.session_state.initialized = True

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AegisAI Threat Analysis",
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
        radial-gradient(circle at 50% 15%, rgba(0, 170, 255, 0.05), transparent 50%),
        radial-gradient(circle at 85% 85%, rgba(0, 255, 136, 0.03), transparent 45%),
        #030611 !important;
}
header, footer, #MainMenu {
    visibility: hidden;
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER & LIVE CLOCK
# =========================================================
st.title("📊 Threat Analysis")
st.caption(f"Analytics Updated: {datetime.now().strftime('%d %b %Y %H:%M:%S')}")

st.write("")

# =========================================================
# TELEMETRY DATA PIPELINES (DYNAMIC MAY 2026 CALCULATOR)
# =========================================================
attack_types = ["DDoS", "Port Scan", "Brute Force", "Web Attack", "Botnet", "Infiltration"]

# DYNAMIC DATES: Automatically anchor data range steps directly inside May 2026
base_historical_start = datetime(2026, 5, 16)
timeline = pd.DataFrame({
    "Day": [base_historical_start + timedelta(days=x) for x in range(7)],
    "DDoS": np.random.randint(50, 200, 7),
    "Port Scan": np.random.randint(20, 120, 7),
    "Brute Force": np.random.randint(10, 90, 7)
})

# ---------------------------------------------------------
# ATTACK TIMELINE LINE CHART
# ---------------------------------------------------------
fig = px.line(
    timeline,
    x="Day",
    y=["DDoS", "Port Scan", "Brute Force"],
    title="Historical Attack Vector Timeline"
)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white")
)
st.plotly_chart(fig, width="stretch")

dist = pd.DataFrame({
    "Attack": attack_types,
    "Count": np.random.randint(50, 300, len(attack_types))
})

# ---------------------------------------------------------
# DISTRIBUTION METRIC CHARTS
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    pie = px.pie(
        dist,
        names="Attack",
        values="Count",
        title="Threat Distribution Matrix"
    )
    pie.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    st.plotly_chart(pie, width="stretch")

with col2:
    bar = px.bar(
        dist,
        x="Attack",
        y="Count",
        color="Attack",
        title="Vector Strike Volume Counts"
    )
    bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    st.plotly_chart(bar, width="stretch")

# ---------------------------------------------------------
# HEATMAP HOURLY VECTOR DENSITY
# ---------------------------------------------------------
heatmap_data = np.random.randint(0, 100, (7, 24))

heatmap = px.imshow(
    heatmap_data,
    labels=dict(x="Hour of Day", y="Day of Week", color="Threats"),
    title="Hourly Attack Density Heatmap Matrix"
)
heatmap.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white")
)
st.plotly_chart(heatmap, width="stretch")

# ---------------------------------------------------------
# TOP TARGET SOURCE RECONNAISSANCE
# ---------------------------------------------------------
attackers = pd.DataFrame({
    "Source IP": [f"192.168.1.{i}" for i in range(1, 11)],
    "Country": np.random.choice(["US", "India", "Germany", "China"], 10),
    "Attack Count": np.random.randint(10, 300, 10),
    "Last Seen": [(datetime(2026, 5, 22) - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(10)],
    "Most Common Attack": np.random.choice(attack_types, 10)
})

st.subheader("🎯 Top Attackers Malicious Telemetry")
st.dataframe(
    attackers,
    width="stretch"
)