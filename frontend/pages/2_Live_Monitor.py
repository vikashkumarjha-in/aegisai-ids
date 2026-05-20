import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import random
from streamlit_autorefresh import st_autorefresh
from utils.styles import load_css
load_css()
st_autorefresh(interval=2000, key="live_monitor_refresh")
st.title("🛰️ Live Threat Monitor"
)
threat_level = random.randint(10, 95)
fig = go.Figure(go.Indicator(
mode="gauge+number",
value=threat_level,
title={'text': "Current Threat Level"},
gauge={
'axis': {'range': [0, 100]},
'bar': {'color': "red"},
'steps': [
{'range': [0, 40], 'color': "green"},
{'range': [40, 70], 'color': "orange"},
{'range': [70, 100], 'color': "red"},
],
}
))
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

packets = np.random.randint(100, 1000, 30)
time_axis = list(range(30))
line_fig = px.line(
x=time_axis,
y=packets,
title="Packets/sec"
)
line_fig.update_layout(template="plotly_dark")
st.plotly_chart(line_fig, use_container_width=True)
st.subheader("🌐 Network Activity"
)
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
title="3D Network Graph"
)
network_fig.update_layout(template="plotly_dark")
st.plotly_chart(network_fig, use_container_width=True)
st.subheader("📦 Live Packets"
)
st.dataframe(
st.session_state.packet_history.head(30),
use_container_width=True,
height=400
)