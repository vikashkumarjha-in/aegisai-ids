import streamlit as st

from streamlit_autorefresh import st_autorefresh

import random

import utils.api as api

# =========================
# AUTO REFRESH
# =========================

st_autorefresh(
    interval=3000,
    key="monitor_refresh"
)

st.title("Live Threat Monitor")

# =========================
# CHECK BACKEND
# =========================

if not api.check_health():

    st.error("Backend Offline")

    st.stop()

# =========================
# SIMULATED TRAFFIC
# =========================

packet = {

    "src_bytes": random.randint(50, 5000),

    "dst_bytes": random.randint(10, 2000),

    "count": random.randint(1, 512)
}

# =========================
# SEND TO API
# =========================

result = api.predict(packet)

# =========================
# HANDLE RESPONSE
# =========================

if "error" in result:

    st.error(f"Backend error: {result['error']}")

else:

    prediction = result.get("prediction", "unknown")

    alert = result.get("alert", {})

    severity = alert.get("severity", "unknown")

    message = alert.get("message", "No message")

    st.subheader("Live Packet")

    st.json(packet)

    if prediction == "attack":

        st.error(message)

        st.warning(f"Severity: {severity.upper()}")

    else:

        st.success(message)

        st.info(f"Severity: {severity.upper()}")