# frontend/Home.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import random

current_time = datetime.now().strftime("%d %b %Y | %H:%M:%S")

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AegisAI IDS Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core Platform Heartbeat Synchronization Loop (3s intervals)
st_autorefresh(interval=3000, key="soc_home_heartbeat")

# =========================================================
# MAXIMUM AGGRESSIVE CYBERPUNK HUD SIDEBAR & CANVAS FIX
# =========================================================
st.markdown("""
<style>
/* Global Canvas Adjustments */
html, body, [class*="css"] {
    background-color: #030611 !important;
    color: #e2f1f7 !important;
    font-family: 'Consolas', 'Segoe UI', monospace, sans-serif;
}

/* Base canvas background depth matrix */
.stApp {
    background: 
        radial-gradient(circle at 15% 15%, rgba(0, 255, 136, 0.05), transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(0, 170, 255, 0.06), transparent 45%),
        #030611 !important;
}

/* --- HARD CORE SIDEBAR OVERRIDES --- */
/* Target the main sidebar container panel */
section[data-testid="stSidebar"] {
    background-color: #04091a !important;
    border-right: 1px solid rgba(0, 255, 255, 0.2) !important;
    box-shadow: 5px 0 25px rgba(0,0,0,0.6) !important;
}

/* Target internal container blocks */
section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    background-color: #04091a !important;
}

/* Force side menu text color and font style to match your HUD */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li div a span {
    color: #c4d6ed !important;
    font-family: 'Consolas', monospace !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}

/* Target fallback link styling for newer Streamlit versions */
section[data-testid="stSidebar"] [data-testid="stSidebarNavItems"] a span {
    color: #c4d6ed !important;
    font-family: 'Consolas', monospace !important;
    font-weight: 600 !important;
}

/* Style the active selected tab item indicator */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li div[data-selected="true"],
section[data-testid="stSidebar"] [data-testid="stSidebarNavItems"] a[aria-current="page"] {
    background-color: rgba(0, 255, 255, 0.12) !important;
    border-left: 3px solid #00ffff !important;
}

/* Hover effects over the sidebar navigation list options */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li div:hover,
section[data-testid="stSidebar"] [data-testid="stSidebarNavItems"] a:hover {
    background-color: rgba(0, 255, 255, 0.05) !important;
}

/* Structural Layout Cleansers */
header, footer, #MainMenu {
    visibility: hidden;
    display: none !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 96% !important;
}

/* Custom SOC Header Card Component */
.hero-wrapper {
    background: linear-gradient(90deg, rgba(4,12,32,0.6) 0%, rgba(2,6,16,0) 100%);
    border-left: 3px solid #00ffff;
    padding: 16px 24px;
    margin-bottom: 30px;
    border-radius: 0 8px 8px 0;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #ffffff;
    text-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
}

.hero-subtitle {
    font-size: 14px;
    color: #8fa0b5;
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    display: flex;
    align-items: center;
}

/* Immersive Neon Glass Metrics Elements */
.metric-card {
    background: linear-gradient(135deg, rgba(8,16,36,0.85) 0%, rgba(4,8,20,0.9) 100%);
    border: 1px solid rgba(0, 255, 255, 0.15);
    padding: 22px;
    border-radius: 6px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(0, 255, 255, 0.4);
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.15);
}

.metric-title {
    color: #627d98;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    margin-top: 10px;
    color: #ffffff;
    font-family: 'Consolas', monospace;
}

.metric-green { color: #00ff88; text-shadow: 0 0 10px rgba(0,255,136,0.3); }
.metric-red { color: #ff3b61; text-shadow: 0 0 10px rgba(255,59,97,0.3); }
.metric-orange { color: #ff9f1c; text-shadow: 0 0 10px rgba(255,159,28,0.3); }

/* Live Pulsing Radar Beacon Animation */
.live-indicator {
    width: 8px;
    height: 8px;
    background: #00ff88;
    border-radius: 50%;
    display: inline-block;
    margin-right: 10px;
    box-shadow: 0 0 10px #00ff88;
    animation: pulse 1.6s infinite ease-in-out;
}

@keyframes pulse {
    0% { transform: scale(0.9); opacity: 1; box-shadow: 0 0 4px #00ff88; }
    50% { transform: scale(1.4); opacity: 0.4; box-shadow: 0 0 14px #00ff88; }
    100% { transform: scale(0.9); opacity: 1; box-shadow: 0 0 4px #00ff88; }
}

.section-title {
    font-size: 16px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 18px;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #8fa0b5;
    border-left: 2px solid #00aaff;
    padding-left: 10px;
}

/* Streamlined Live Attack Terminal Feed Frame */
.attack-feed {
    background: rgba(5, 10, 20, 0.88) !important;
    border: 1px solid rgba(0, 255, 255, 0.12) !important;
    border-radius: 8px;
    padding: 18px;
    height: 390px;
    overflow: hidden;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(0,255,255,0.03);
}

.feed-item {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 12px;
    padding: 12px 0 !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
}

.feed-item:last-child {
    border-bottom: none !important;
}

.feed-time {
    color: #00aaff !important;
    font-size: 11px !important;
    min-width: 72px;
    font-family: Consolas, monospace !important;
}

.feed-text {
    flex: 1;
    color: #dbeafe !important;
    font-size: 13px !important;
    line-height: 1.5 !important;
}

.feed-status {
    min-width: 85px;
    text-align: center;
}

/* Dynamic Interactive Module Launcher Grid Styles */
.module-tile {
    background: linear-gradient(145deg, rgba(6,14,32,0.8) 0%, rgba(3,6,16,0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    padding: 20px 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    height: 160px;               /* Strict height alignment control */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
}

.module-tile:hover {
    border-color: #00ffff;
    background: linear-gradient(145deg, rgba(0,255,255,0.05) 0%, rgba(3,6,16,0.9) 100%);
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# PLATFORM ARTIFACT MATRICES & MOCK DATA SETUP
# =========================================================
attack_vectors = ["DDoS Mitigation", "Port Sweep Scan", "Botnet Check-In", "Web Exploitation", "SSH BruteForce", "SQL Injection", "Network Infiltration"]
global_regions = ["United States", "China", "Russian Federation", "India", "Germany", "Brazil", "United Kingdom", "Japan", "France", "Australia"]

# Supplementary Sidebar Text Header
with st.sidebar:
    st.markdown("<br><p style='text-align:center; color:#00ffff;'>🔒 ENGINES ACTIVE</p>", unsafe_allow_html=True)
    st.markdown("---")

# =========================================================
# SOC PLATFORM HEADER OVERLAY
# =========================================================
current_time = datetime.now().strftime("%d %b %Y | %H:%M:%S")

hero_html = f"""
<div class="hero-wrapper">
    <div class="hero-title">
        🛡️ AEGIS.AI SYSTEM DASHBOARD
    </div>
    <div class="hero-subtitle">
        <span class="live-indicator"></span>
        LIVE SECURITY OPERATIONS CENTER &nbsp;|&nbsp; {current_time} UTC
    </div>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)

# =========================================================
# TELEMETRY COUNTER ROW COMPONENTS
# =========================================================
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Network Flows Analyzed</div>
        <div class="metric-value">{np.random.randint(142000, 168000):,}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Active Security Threats</div>
        <div class="metric-value metric-red">{np.random.randint(14, 38)}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">In-Flight Blocked Malicious IPs</div>
        <div class="metric-value metric-orange">{np.random.randint(1800, 3400):,}</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">AI Core Defense Precision</div>
        <div class="metric-value metric-green">99.42%</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PRIMARY DATA ANALYTICS LAYOUT SECTION
# =========================================================
left_pane, right_pane = st.columns([2, 1])

# =========================================================
# LEFT PANE : THREAT GRAPH
# =========================================================
with left_pane:
    st.markdown(
        '<div class="section-title">📊 Real-Time Threat Intrusion Activity (24H Trend)</div>',
        unsafe_allow_html=True
    )

    time_index = pd.date_range(
        datetime.now() - timedelta(hours=12),
        periods=36,
        freq="20min"
    )

    threat_amplitude = np.random.randint(15, 95, size=36)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=time_index,
            y=threat_amplitude,
            mode="lines",
            fill="tozeroy",
            line=dict(color="#00ffff", width=2.5),
            fillcolor="rgba(0,255,255,0.05)"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)", title="Threat Events")
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )

# =========================================================
# RIGHT PANE : LIVE TELEMETRY FEED
# =========================================================
with right_pane:
    st.markdown(
        '<div class="section-title">🚨 System Telemetry Feed</div>',
        unsafe_allow_html=True
    )

    feed_elements = []
    feed_elements.append('<div class="attack-feed">')

    for index in range(6):
        selected_attack = random.choice(attack_vectors)
        origin_country = random.choice(global_regions)
        target_country = random.choice([c for c in global_regions if c != origin_country])
        
        timestamp_string = (datetime.now() - timedelta(seconds=random.randint(2, 180))).strftime("%H:%M:%S")

        # Severity Assessment
        if selected_attack in ["DDoS Mitigation", "Network Infiltration"]:
            status_text = "CRITICAL"
            hex_color = "#ff3b61"
        elif selected_attack in ["SQL Injection", "Web Exploitation"]:
            status_text = "HIGH"
            hex_color = "#ff9f1c"
        else:
            status_text = "WARNING"
            hex_color = "#00aaff"

        # Concat string flatly without raw inner carriage returns
        row_string = (
            '<div class="feed-item">'
                '<div class="feed-time">[' + timestamp_string + ']</div>'
                '<div class="feed-text">'
                    '<span style="color:' + hex_color + '; margin-right:6px; font-weight:bold;">●</span>'
                    '<strong>' + selected_attack + '</strong><br>'
                    '<span style="color:#627d98; font-size:11px;">' + origin_country + ' &rarr; ' + target_country + '</span>'
                '</div>'
                '<div class="feed-status" style="color:' + hex_color + '; border:1px solid ' + hex_color + '30; background:' + hex_color + '10; padding:4px 10px; border-radius:4px; font-size:10px; font-weight:bold;">' + status_text + '</div>'
            '</div>'
        )
        feed_elements.append(row_string)

    feed_elements.append('</div>')
    
    st.markdown("".join(feed_elements), unsafe_allow_html=True)

# =========================================================
# BOTTOM SECTION: PLATFORM MODULES LAUNCHER GRID
# =========================================================
st.markdown('<div class="section-title">🌐 Platform Operational Modules</div>', unsafe_allow_html=True)

sub_columns = st.columns(5)
operational_modules = [
    ("📊", "Dashboard Metrics"),
    ("📡", "Live Interceptor"),
    ("🧠", "AI Threat Analyzer"),
    ("📜", "System Log Registry"),
    ("🌍", "Global Attack Map")
]

for column, module_info in zip(sub_columns, operational_modules):
    with column:
        st.markdown(f"""
        <div class="module-tile">
            <div style="font-size:36px; margin-bottom:8px;">{module_info[0]}</div>
            <div style="font-size:14px; font-weight:600; color:#ffffff; letter-spacing:0.5px; min-height:36px; display:flex; align-items:center; justify-content:center;">
                {module_info[1]}
            </div>
            <div style="font-size:10px; color:#486581; margin-top:6px; text-transform:uppercase; font-weight:700;">Status: Active</div>
        </div>
        """, unsafe_allow_html=True)