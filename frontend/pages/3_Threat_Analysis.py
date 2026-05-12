import streamlit as st
import plotly.express as px
import pandas as pd

st.title("📈 Threat Analytics")

data = pd.DataFrame({
    "Type": ["DoS", "Probe", "Brute Force"],
    "Count": [10, 5, 8]
})

fig = px.bar(data, x="Type", y="Count", color="Type")
st.plotly_chart(fig)