# frontend/pages/1_Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from utils.styles import load_css
from utils.data_generator import generate_event
import random
from datetime import datetime

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
    page_title="AegisAI Dashboard",
    layout="wide"
)

load_css()

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
        radial-gradient(circle at 15% 15%, rgba(0, 255, 136, 0.05), transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(0, 170, 255, 0.06), transparent 45%),
        #030611 !important;
}
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(8,16,36,0.85) 0%, rgba(4,8,20,0.9) 100%) !important;
    border: 1px solid rgba(0, 255, 255, 0.15) !important;
    padding: 15px 20px !important;
    border-radius: 6px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
}
div[data-testid="stMetric"]:hover {
    border-color: rgba(0, 255, 255, 0.4) !important;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.15) !important;
}
div[data-testid="stMetric"] label {
    color: #627d98 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    font-weight: 600 !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    font-family: 'Consolas', monospace !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# AUTO REFRESH
# =========================================================
st_autorefresh(interval=2000, key="dashboard_refresh")

if "dashboard_initialized" not in st.session_state:
    st.session_state.dashboard_initialized = False

# =========================================================
# GENERATE INITIAL DATA
# =========================================================
if not st.session_state.dashboard_initialized or st.session_state.logs.empty:
    initial_events = []
    for _ in range(120):
        event = generate_event()
        initial_events.append(event)
        if event.get("Severity") == "Critical":
            st.session_state.blocked_ips.add(event.get("Source IP"))
    initial_df = pd.DataFrame(initial_events)
    st.session_state.logs = initial_df.copy()
    st.session_state.packet_history = initial_df.copy()
    st.session_state.dashboard_initialized = True

# =========================================================
# LIVE EVENT GENERATION
# =========================================================
new_event = generate_event()
new_df = pd.DataFrame([new_event])

st.session_state.logs = pd.concat([new_df, st.session_state.logs], ignore_index=True)
st.session_state.packet_history = pd.concat([new_df, st.session_state.packet_history], ignore_index=True)

st.session_state.logs = st.session_state.logs.head(500)
st.session_state.packet_history = st.session_state.packet_history.head(500)

if new_event.get("Severity") == "Critical":
    st.session_state.blocked_ips.add(new_event.get("Source IP"))

# =========================================================
# HEADER
# =========================================================
st.title("📊 Security Dashboard")
st.caption(f"Last Updated: {datetime.now().strftime('%d %b %Y %H:%M:%S')}")

st.markdown(
    """
    <div style='color:#9aa4b2; margin-bottom:20px; font-size:14px; text-transform:uppercase; letter-spacing:1px;'>
    Enterprise Intrusion Detection & Threat Monitoring Platform
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LIVE METRICS ENGINE
# =========================================================
total_events = len(st.session_state.logs)
blocked_ips_count = random.randint(1200, 3500)
ai_confidence = round(random.uniform(94.1, 99.8), 2)
system_status = random.choice(["ACTIVE", "MONITORING", "SECURE"])

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "🚨 Total Threats",
        f"{total_events:,}",
        delta=f"+{random.randint(2,12)}"
    )

with m2:
    st.metric(
        "⛔ Blocked IPs",
        f"{blocked_ips_count:,}",
        delta=f"+{random.randint(1,9)}"
    )

with m3:
    st.metric(
        "🧠 AI Confidence",
        f"{ai_confidence}%",
        delta="+0.2%"
    )

with m4:
    st.metric(
        "🟢 System Status",
        system_status
    )

# =========================================================
# LIVE ALERTS
# =========================================================
st.write("")
st.subheader("🚨 Live Security Alerts")

if not st.session_state.logs.empty and "Severity" in st.session_state.logs.columns:
    alerts = st.session_state.logs[st.session_state.logs["Severity"].isin(["Critical", "High"])]
else:
    alerts = pd.DataFrame()

st.dataframe(
    alerts.head(8),
    use_container_width=True,
    height=320
)

# =========================================================
# CHARTS
# =========================================================
col1, col2 = st.columns(2)

with col1:
    if not st.session_state.logs.empty and "Attack Type" in st.session_state.logs.columns:
        attack_counts = st.session_state.logs["Attack Type"].value_counts().reset_index()
        attack_counts.columns = ["Attack Type", "Count"]
    else:
        attack_counts = pd.DataFrame(columns=["Attack Type", "Count"])

    pie = px.pie(
        attack_counts,
        names="Attack Type",
        values="Count",
        title="Threat Distribution"
    )
    pie.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    st.plotly_chart(pie, use_container_width=True)

with col2:
    bar = px.bar(
        attack_counts,
        x="Attack Type",
        y="Count",
        color="Attack Type",
        title="Attack Counts"
    )
    bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    st.plotly_chart(bar, use_container_width=True)

# =========================================================
# LIVE PACKET HISTORY
# =========================================================
st.subheader("📡 Live Packet History")

available_cols = list(st.session_state.packet_history.columns)
target_cols = [
    "Timestamp", "Source IP", "Destination IP", "Dest Port", "Protocol", 
    "Bytes", "Packets", "Attack Type", "Severity", "Action", "Country"
]
valid_cols = [col for col in target_cols if col in available_cols]

if valid_cols:
    packet_display = st.session_state.packet_history[valid_cols].head(50)
else:
    packet_display = st.session_state.packet_history.head(50)

st.dataframe(
    packet_display,
    use_container_width=True,
    height=420
)

# =========================================================
# LIVE TRAFFIC GRAPH
# =========================================================
st.subheader("📈 Packets / Second")

traffic_data = pd.DataFrame({
    "Time": list(range(30)),
    "Packets": [400 + (i * 5) + (i % 3) * 40 for i in range(30)]
})

traffic_fig = go.Figure()
traffic_fig.add_trace(
    go.Scatter(
        x=traffic_data["Time"],
        y=traffic_data["Packets"],
        mode="lines",
        fill="tozeroy",
        name="Traffic",
        line=dict(color="#00aaff")
    )
)
traffic_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    height=350
)
st.plotly_chart(traffic_fig, use_container_width=True)

# =========================================================
# SECURITY EVENT STREAM
# =========================================================
st.subheader("⚡ Live Security Event Stream")

event_box = st.container(border=True)
with event_box:
    event_elements = []
    for _, row in st.session_state.logs.head(12).iterrows():
        current_sev = row.get("Severity", "Benign")
        attack_type = row.get("Attack Type", "Unknown")
        source_ip = row.get("Source IP", "0.0.0.0")
        dest_port = row.get("Dest Port", row.get("Destination Port", "N/A"))
        timestamp = row.get("Timestamp", "N/A")
        confidence = row.get("AI Confidence", "100")

        severity_color = {
            "Critical": "#ff1744",
            "High": "#ff9100",
            "Medium": "#ffd600",
            "Benign": "#00e676"
        }.get(current_sev, "#00e676")

        row_html = (
            f'<div style="padding:10px; margin-bottom:8px; border-left:4px solid {severity_color}; '
            f'background:#060e20; border:1px solid rgba(255,255,255,0.05); border-radius:6px;">'
            f'<b>{str(attack_type)}</b> detected from '
            f'<span style="color:#00e5ff">{str(source_ip)}</span> &arr; '
            f'<span style="color:#8bc34a">Port {str(dest_port)}</span><br>'
            f'<small style="color:#9ca3af">{str(timestamp)} | Severity: {str(current_sev)} | '
            f'Confidence: {str(confidence)}%</small>'
            f'</div>'
        )
        event_elements.append(row_html)
    st.markdown("".join(event_elements), unsafe_allow_html=True)

# =========================================================
# SYSTEM STATUS
# =========================================================
st.subheader("🖥️ System Status")

sys1, sys2, sys3, sys4 = st.columns(4)
with sys1:
    st.success("Detection Engine Active")
with sys2:
    st.success("Packet Capture Running")
with sys3:
    st.success("Threat Intelligence Synced")
with sys4:
    st.success("ML Model Operational")