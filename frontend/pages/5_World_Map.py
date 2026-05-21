# frontend/pages/5_World_Map.py

import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="AegisAI Cyberthreat Map", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# =========================================================
# INITIALIZE NAVIGATION & ZOOM CONTROLS IN SESSION STATE
# =========================================================
if 'map_zoom' not in st.session_state:
    st.session_state.map_zoom = 0.65

if 'map_pitch' not in st.session_state:
    st.session_state.map_pitch = 38

if 'deg_spin' not in st.session_state:
    st.session_state.deg_spin = 0
else:
    # Continuously rotate map if globe view is active
    if st.session_state.get('auto_rotate', True):
        st.session_state.deg_spin = (st.session_state.deg_spin + 3) % 360

# Safe conversion calculation for Pydeck wrap limits
bound_longitude = (st.session_state.deg_spin + 180 % 360) - 180

# =========================================================
# SYSTEM OVERLAY INTERFACE STYLING
# =========================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    margin: 0;
    padding: 0;
    overflow: hidden !important;
    background: #010308 !important;
    font-family: 'Consolas', 'Courier New', monospace;
}

header, footer, #MainMenu, [data-testid="collapsedControl"] { 
    visibility: hidden; 
    display: none !important;
}

section[data-testid="stSidebar"] { 
    display: none !important; 
}

.main .block-container { 
    padding: 0 !important; 
    max-width: 100vw !important; 
    margin: 0 !important;
}

.stApp { 
    background: radial-gradient(ellipse at center, #050b14 0%, #010307 100%);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300' viewBox='0 0 300 300'%3E%3Ccircle cx='15' cy='35' r='0.6' fill='%2300ffff' opacity='0.6'/%3E%3Ccircle cx='85' cy='15' r='0.4' fill='%23ffffff' opacity='0.4'/%3E%3Ccircle cx='140' cy='95' r='0.5' fill='%23ffffff' opacity='0.7'/%3E%3Ccircle cx='220' cy='45' r='0.7' fill='%23ff00ff' opacity='0.5'/%3E%3Ccircle cx='60' cy='180' r='0.4' fill='%23ffffff' opacity='0.5'/%3E%3Ccircle cx='190' cy='130' r='0.6' fill='%2300ffff' opacity='0.4'/%3E%3Ccircle cx='270' cy='210' r='0.5' fill='%23ffffff' opacity='0.8'/%3E%3Ccircle cx='110' cy='260' r='0.8' fill='%23ffffff' opacity='0.6'/%3E%3C/svg%3E");
    background-repeat: repeat;
}

.cyber-header {
    position: fixed;
    top: 25px;
    left: 40px;
    z-index: 9999;
    color: #e2f7ff;
    letter-spacing: 3px;
    font-size: 20px;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.6);
}

.corner-feed {
    position: fixed; 
    bottom: 95px; 
    left: 40px; 
    width: 420px;
    background: rgba(2, 6, 16, 0.85); 
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(0, 255, 255, 0.25); 
    border-radius: 4px;
    padding: 20px; 
    z-index: 9998; 
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.8);
}

.feed-title {
    color: #00ffff; 
    font-size: 13px; 
    margin-bottom: 16px;
    text-transform: uppercase; 
    letter-spacing: 2px; 
    font-weight: bold;
    border-bottom: 1px solid rgba(0, 255, 255, 0.15);
    padding-bottom: 6px;
}

.feed-item { display: flex; margin-bottom: 14px; align-items: flex-start; }
.feed-dot { width: 8px; height: 8px; border-radius: 50%; margin-right: 14px; flex-shrink: 0; margin-top: 4px; box-shadow: 0 0 12px currentColor; }
.feed-text { color: #d1e2eb; font-size: 12px; line-height: 1.4; }
.feed-meta { color: #627d98; font-size: 11px; margin-top: 2px; }

/* Fixed Control Column Button Triggers styling override */
.control-rack {
    position: fixed;
    top: 30px;
    right: 40px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.stButton > button {
    width: 44px !important;
    height: 44px !important;
    background: rgba(4, 10, 22, 0.85) !important;
    border: 1px solid rgba(0, 255, 255, 0.3) !important;
    color: #00ffff !important;
    border-radius: 4px !important;
    font-size: 16px !important;
    padding: 0 !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: rgba(0, 255, 255, 0.25) !important;
    border-color: #00ffff !important;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.5) !important;
}

.bottom-hud {
    position: fixed; 
    bottom: 25px; 
    left: 50%; 
    transform: translateX(-50%);
    display: flex; 
    background: rgba(3, 8, 20, 0.85); 
    border: 1px solid rgba(255, 255, 255, 0.1); 
    z-index: 9999;
    backdrop-filter: blur(15px);
    border-radius: 4px;
    box-shadow: 0 0 25px rgba(0,0,0,0.6);
}

.hud-btn { padding: 12px 28px; color: #486581; font-size: 12px; font-weight: 600; border-right: 1px solid rgba(255, 255, 255, 0.08); letter-spacing: 1.5px; }
.hud-btn:last-child { border-right: none; }
.hud-btn.active-mav { color: #ff5500; text-shadow: 0 0 12px #ff5500; }
.hud-btn.active-wav { color: #00aaff; text-shadow: 0 0 12px #00aaff; }
.hud-btn.active-ids { color: #ff0088; text-shadow: 0 0 12px #ff0088; }
.hud-btn.active-oas { color: #00ff88; text-shadow: 0 0 12px #00ff88; }

[data-testid="stDeckGlJsonChart"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# GLOBAL STREAM TIMING (1.5s Interval Refresh)
# =========================================================
st_autorefresh(interval=1500, key="aegis_runtime_engine")

# =========================================================
# THREAT ARRAYS: EXTENDED TO 10 GLOBAL ACTIVE COUNTRIES
# =========================================================
def generate_broad_telemetry():
    countries = {
        "USA": [37.0902, -95.7129],
        "China": [35.8617, 104.1954], 
        "Russia": [61.5240, 105.3188], 
        "India": [20.5937, 78.9629],
        "Brazil": [-14.2350, -51.9253], 
        "UK": [55.3781, -3.4360],
        "Japan": [36.2048, 138.2529], 
        "South Africa": [-30.5595, 22.9375],
        "Germany": [51.1657, 10.4515], 
        "Australia": [-25.2744, 133.7751]
    }
    
    detections = {
        "MAV": {"color": [255, 85, 0], "name": "Trojan.Win32.Generic"},
        "WAV": {"color": [0, 170, 255], "name": "HEUR:Exploit.Script"},
        "IDS": {"color": [255, 0, 136], "name": "Intrusion.Win.MS17-010"},
        "OAS": {"color": [0, 255, 136], "name": "Backdoor.Linux.Mirai"},
    }
    
    pillars = []
    for _ in range(180): # Densified cluster nodes
        country = np.random.choice(list(countries.keys()))
        dtype = np.random.choice(list(detections.keys()))
        lat, lon = countries[country]
        pillars.append({
            "lat": lat + np.random.uniform(-4.5, 4.5),
            "lon": lon + np.random.uniform(-4.5, 4.5),
            "elevation": np.random.randint(250000, 3400000),
            "detection_type": dtype,
            "color_r": detections[dtype]["color"][0],
            "color_g": detections[dtype]["color"][1],
            "color_b": detections[dtype]["color"][2],
        })
        
    arcs = []
    for _ in range(35): # Expanded tracking paths across all 10 countries
        src, dst = np.random.choice(list(countries.keys()), 2, replace=False)
        dtype = np.random.choice(list(detections.keys()))
        arcs.append({
            "src_lat": countries[src][0], "src_lon": countries[src][1],
            "dst_lat": countries[dst][0], "dst_lon": countries[dst][1],
            "detection_type": dtype,
            "attack_name": detections[dtype]["name"],
            "src_country": src, "dst_country": dst,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "color_r": detections[dtype]["color"][0],
            "color_g": detections[dtype]["color"][1],
            "color_b": detections[dtype]["color"][2],
            "width": np.random.randint(2, 6)
        })
        
    return pd.DataFrame(pillars), pd.DataFrame(arcs)

df_pillars, df_arcs = generate_broad_telemetry()

# =========================================================
# INTERACTIVE BUTTON HANDLERS (Alters view state on loop)
# =========================================================
def toggle_rotation():
    st.session_state.auto_rotate = not st.session_state.get('auto_rotate', True)

def trigger_zoom_in():
    st.session_state.map_zoom = min(st.session_state.map_zoom + 0.15, 3.0)

def trigger_zoom_out():
    st.session_state.map_zoom = max(st.session_state.map_zoom - 0.15, 0.35)

# Render operational state buttons behind stylized structural wrappers
with st.container():
    st.markdown('<div class="control-rack">', unsafe_allow_html=True)
    st.button("🌐", on_click=toggle_rotation, key="btn_rot")
    st.button("＋", on_click=trigger_zoom_in, key="btn_zi")
    st.button("－", on_click=trigger_zoom_out, key="btn_zo")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# PYDECK SPATIAL VISUALIZATION LAYERS
# =========================================================
geojson_map_url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson"

world_topology = pdk.Layer(
    "GeoJsonLayer",
    geojson_map_url,
    stroked=True,
    filled=True,
    get_line_color=[0, 255, 255, 35], 
    get_fill_color=[6, 16, 38, 160],  
    line_width_min_pixels=1,
)

pillar_layer = pdk.Layer(
    "ColumnLayer",
    data=df_pillars,
    get_position=["lon", "lat"],
    get_elevation="elevation",
    elevation_scale=1,
    radius=85000,
    get_fill_color=["color_r", "color_g", "color_b", 200],
)

arc_layer = pdk.Layer(
    "ArcLayer",
    data=df_arcs,
    get_source_position=["src_lon", "src_lat"],
    get_target_position=["dst_lon", "dst_lat"],
    get_source_color=["color_r", "color_g", "color_b", 80],
    get_target_color=["color_r", "color_g", "color_b", 240],
    get_width="width",
)

# ViewState reads properties from live updated Session State configurations
view_matrix = pdk.ViewState(
    latitude=22, 
    longitude=bound_longitude, 
    zoom=st.session_state.map_zoom, 
    pitch=st.session_state.map_pitch, 
    bearing=5
)

deck_canvas = pdk.Deck(
    layers=[world_topology, pillar_layer, arc_layer],
    initial_view_state=view_matrix,
    map_provider=None, 
    views=[pdk.View(type="GlobeView", controller=False)],
    parameters={"blend": True}
)

st.pydeck_chart(deck_canvas, use_container_width=True, height=940)

# =========================================================
# TITLE & TELEMETRY LIVE TICKER INJECTIONS
# =========================================================
st.markdown('<div class="cyber-header">☰ AEGIS.AI // LIVE THREAT TELEMETRY</div>', unsafe_allow_html=True)

html_ticker_accumulator = '<div class="corner-feed"><div class="feed-title">REALTIME DETECTION ENGINE</div>'
for _, entry in df_arcs.head(6).iterrows():
    rgb_string = f"rgb({int(entry['color_r'])}, {int(entry['color_g'])}, {int(entry['color_b'])})"
    
    html_ticker_accumulator += (
        f'<div class="feed-item">'
        f'  <div class="feed-dot" style="background:{rgb_string}; color:{rgb_string};"></div>'
        f'  <div class="feed-text">'
        f'    <strong>{str(entry["attack_name"])}</strong><br>'
        f'    <div class="feed-meta">{str(entry["timestamp"])} | {str(entry["src_country"])} &rarr; {str(entry["dst_country"])} [{str(entry["detection_type"])}]</div>'
        f'  </div>'
        f'</div>'
    )
html_ticker_accumulator += '</div>'
st.markdown(html_ticker_accumulator, unsafe_allow_html=True)

# Footer Analytics HUD Frame
st.markdown(f"""
<div class="bottom-hud">
  <div class="hud-btn">◀ CONTROLS</div>
  <div class="hud-btn active-mav">MAV {np.random.randint(280000, 420000)}</div>
  <div class="hud-btn active-wav">WAV {np.random.randint(650000, 850000)}</div>
  <div class="hud-btn active-ids">IDS {np.random.randint(110000, 250000)}</div>
  <div class="hud-btn active-oas">OAS {np.random.randint(450000, 600000)}</div>
  <div class="hud-btn">DIAGNOSTICS ▶</div>
</div>
""", unsafe_allow_html=True)