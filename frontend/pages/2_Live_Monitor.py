import streamlit as st
import time

st.title("🔴 Live Threat Monitor")

placeholder = st.empty()

for i in range(10):
    with placeholder.container():
        st.warning("Suspicious traffic detected")
        st.write("Packet analysis running...")

    time.sleep(2)