import streamlit as st
import random
import pandas as pd
import datetime as dt
from streamlit_autorefresh import st_autorefresh
import utils.api as api

# ===============================
# MODULE 4 — UI / PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="AegisAI SOC Command Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp { background-color: #F8FAFC; color: #0F172A; }
section[data-testid="stSidebar"] { background-color: #E2E8F0; }
h1, h2, h3 { color: #0F172A !important; font-weight: 700; }
div[data-testid="stMetric"] {
    background-color: #FFFFFF; border: 1px solid #CBD5E1;
    padding: 14px; border-radius: 12px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.08);
}
div[data-testid="stMetricValue"] { color: #0F172A; font-weight: 700; }
.stButton > button {
    background-color: #2563EB !important; color: white !important;
    border-radius: 10px !important; font-weight: 600 !important; border: none !important;
}
.stButton > button:hover { background-color: #1D4ED8 !important; }
.dataframe { background-color: white; color: #0F172A; }
.stAlert { border-radius: 10px; }
.stSuccess { border-left: 5px solid #22C55E; }
.stWarning { border-left: 5px solid #F59E0B; }
.stError { border-left: 5px solid #EF4444; }
hr { border: 1px solid #E2E8F0; }
</style>
""", unsafe_allow_html=True)

# Auto refresh every 3 seconds
st_autorefresh(interval=3000, key="soc_refresh")

# Sidebar
st.sidebar.title("AegisAI SOC")
backend_online = api.check_health()

if backend_online:

    st.sidebar.success("Backend: Connected")

else:

    st.sidebar.error("Backend: Offline")
st.sidebar.caption("Frontend: Streamlit Dashboard")

# ===============================
# SESSION STATE INIT
# ===============================
if "logs" not in st.session_state:
    st.session_state.logs = pd.DataFrame(
        columns=["Time", "Source IP", "Attack Type", "Protocol", "Severity"]
    )

if "packet_streaming" not in st.session_state:
    st.session_state.packet_streaming = False

if "packet_history" not in st.session_state:
    st.session_state.packet_history = pd.DataFrame(
        columns=["Time", "Src Bytes", "Dst Bytes", "Count", "Prediction"]
    )

# Helper: generate a sample packet
def generate_packet():
    return {
        "src_bytes": random.randint(50, 5000),
        "dst_bytes": random.randint(10, 2000),
        "count": random.randint(1, 512)
    }

# Helper: append a row to a dataframe
def append_row(df, row):
    return pd.concat([df, pd.DataFrame([row])], ignore_index=True)

# ===============================
# MODULE 1 — SOC DASHBOARD / LIVE STATUS
# ===============================
st.title("🛡️ AEGISAI SECURITY OPERATIONS CENTER")
st.caption("Real-Time Threat Intelligence & AI-Based Intrusion Detection System")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
active_threats = len(st.session_state.logs[st.session_state.logs["Severity"] == "Critical"]) if len(st.session_state.logs) else 0

col1.metric("Active Threats", active_threats)
col2.metric("Blocked IPs", "1,240", "+12")
col3.metric("AI Confidence", "98.2%", "Stable")
col4.metric("System Status", "ONLINE", "Healthy")

st.markdown("---")

st.subheader("🔍 AI Threat Detection Engine")
scan_col1, scan_col2 = st.columns([1, 2])

with scan_col1:
    if st.button("Run Security Scan"):
        sample_packet = generate_packet()
        with st.spinner("Sending packet to AI engine..."):
            result = api.predict(sample_packet)

        if "error" in result:
            st.error("Backend connection failed")
            st.json(result)
        else:
            st.success("Threat analysis completed")
            st.json(sample_packet)
            st.json(result)

with scan_col2:
    st.info("This panel sends a test packet to your deployed FastAPI backend and shows the response here.")

st.markdown("---")

st.subheader("🚨 Live Security Alerts")
alert_type = random.randint(1, 10)
if alert_type > 7:
    st.error("CRITICAL: Possible DDoS Attack Detected")
elif alert_type > 4:
    st.warning("MEDIUM: Suspicious Port Scanning Activity")
else:
    st.success("SYSTEM NORMAL: No active threats detected")

st.markdown("---")

st.subheader("📜 Security Event Stream")
logs = ["TCP packet analyzed","UDP anomaly detected","Normal traffic flow","Suspicious IP checked","Firewall rule applied"]
st.write(f"🕒 {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} → {random.choice(logs)}")

# ===============================
# MODULE 2 — LIVE ATTACK LOGGING SYSTEM
# ===============================
st.markdown("---")
st.subheader("📜 SECURITY OPERATIONS LOGS (LIVE SIEM FEED)")

log_col1, log_col2 = st.columns(2)
with log_col1:
    if st.button("Generate Security Event"):
        new_event = {
            "Time": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Source IP": f"192.168.1.{random.randint(2, 254)}",
            "Attack Type": random.choice(["DDoS","Port Scan","SQL Injection","Brute Force","Normal Traffic"]),
            "Protocol": random.choice(["TCP","UDP","ICMP"]),
            "Severity": random.choice(["Low","Medium","High","Critical"])
        }
        st.session_state.logs = append_row(st.session_state.logs, new_event)
        st.success("New security event logged!")

with log_col2:
    if st.button("Generate Critical Event"):
        critical_event = {
            "Time": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Source IP": f"10.0.0.{random.randint(2, 254)}",
            "Attack Type": random.choice(["DDoS","SQL Injection","Brute Force"]),
            "Protocol": random.choice(["TCP","UDP","ICMP"]),
            "Severity": "Critical"
        }
        st.session_state.logs = append_row(st.session_state.logs, critical_event)
        st.error("Critical event generated!")

st.dataframe(st.session_state.logs, use_container_width=True)

st.markdown("### 🚨 Critical Threats Only")
critical_logs = st.session_state.logs[st.session_state.logs["Severity"] == "Critical"]
if len(critical_logs) > 0:
    st.dataframe(critical_logs, use_container_width=True)
else:
    st.info("No critical threats yet. Use 'Generate Critical Event' to create one.")

st.markdown("### 📊 Threat Distribution")
if len(st.session_state.logs) > 0:
    st.bar_chart(st.session_state.logs["Severity"].value_counts())
else:
    st.info("No logs available yet.")

# ===============================
# MODULE 3 — REAL-TIME PACKET SIMULATION ENGINE
# ===============================
st.markdown("---")
st.subheader("🌐 REAL-TIME NETWORK TRAFFIC SIMULATION (IDS ENGINE)")

sim_col1, sim_col2 = st.columns(2)
with sim_col1:
    if st.button("Start Live Packet Simulation"):
        st.session_state.packet_streaming = True
with sim_col2:
    if st.button("Stop Packet Simulation"):
        st.session_state.packet_streaming = False

if st.session_state.packet_streaming:
    st.success("Live traffic monitoring is running...")
    packet = generate_packet()
    result = api.predict(packet)
    prediction_text = "Error" if "error" in result else str(result)

    packet_row = {
        "Time": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Src Bytes": packet["src_bytes"],
        "Dst Bytes": packet["dst_bytes"],
        "Count": packet["count"],
        "Prediction": prediction_text
    }
    st.session_state.packet_history = append_row(st.session_state.packet_history, packet_row)
    if len(st.session_state.packet_history) > 20:
        st.session_state.packet_history = st.session_state.packet_history.tail(20).reset_index(drop=True)

    st.markdown("#### Latest Packet")
    st.json(packet)

    if "error" in result:
        st.error("Backend Error Detected")
        st.json(result)
    else:
        st.markdown("#### AI Prediction")
        st.json(result)
        if "attack" in str(result).lower():
            st.error("🚨 THREAT DETECTED")
        else:
            st.success("🟢 Normal Traffic")
else:
    st.info("Click 'Start Live Packet Simulation' to begin streaming packets.")

st.markdown("#### Packet History")
