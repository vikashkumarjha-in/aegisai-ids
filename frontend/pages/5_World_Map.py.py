import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.title("🌍 Global Cyber Attack Map")

data = pd.DataFrame({
    "lat": [20, 40, -10, 50, 30],
    "lon": [77, -100, -60, 10, 120],
    "attack": ["DDoS","SQLi","Botnet","Scan","Malware"],
    "intensity": [random.randint(10,100) for _ in range(5)]
})

fig = px.scatter_geo(
    data,
    lat="lat",
    lon="lon",
    color="attack",
    size="intensity",
    projection="natural earth",
    title="Live Global Attack Map"
)

st.plotly_chart(fig, use_container_width=True)