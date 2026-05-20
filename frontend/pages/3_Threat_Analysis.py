import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.styles import load_css

st.set_page_config(layout="wide")

load_css()

st.title("Threat Analysis")

attack_types = [
    "DDoS",
    "Port Scan",
    "Brute Force",
    "Web Attack",
    "Botnet",
    "Infiltration"
]

timeline = pd.DataFrame({
    "Day": pd.date_range("2026-01-01", periods=7),
    "DDoS": np.random.randint(50, 200, 7),
    "Port Scan": np.random.randint(20, 120, 7),
    "Brute Force": np.random.randint(10, 90, 7)
})

fig = px.line(
    timeline,
    x="Day",
    y=["DDoS", "Port Scan", "Brute Force"],
    title="Attack Timeline"
)

st.plotly_chart(fig, use_container_width=True)

dist = pd.DataFrame({
    "Attack": attack_types,
    "Count": np.random.randint(50, 300, len(attack_types))
})

col1, col2 = st.columns(2)

with col1:

    pie = px.pie(
        dist,
        names="Attack",
        values="Count",
        title="Threat Distribution"
    )

    st.plotly_chart(pie, use_container_width=True)

with col2:

    bar = px.bar(
        dist,
        x="Attack",
        y="Count",
        color="Attack",
        title="Attack Counts"
    )

    st.plotly_chart(bar, use_container_width=True)

heatmap_data = np.random.randint(0, 100, (7, 24))

heatmap = px.imshow(
    heatmap_data,
    labels=dict(x="Hour", y="Day", color="Threats"),
    title="Severity Heatmap"
)

st.plotly_chart(heatmap, use_container_width=True)

attackers = pd.DataFrame({
    "Source IP": [f"192.168.1.{i}" for i in range(1, 11)],
    "Country": np.random.choice(
        ["US", "India", "Germany", "China"],
        10
    ),
    "Attack Count": np.random.randint(10, 300, 10),
    "Last Seen": pd.date_range(
        "2026-01-01",
        periods=10
    ),
    "Most Common Attack": np.random.choice(
        attack_types,
        10
    )
})

st.subheader("Top Attackers")

st.dataframe(
    attackers,
    use_container_width=True
)