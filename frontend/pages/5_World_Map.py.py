# ===============================
# 🗺️ MODULE 7 — GLOBAL ATTACK MAP
# ===============================

st.markdown("---")
st.subheader("🗺️ GLOBAL CYBER ATTACK MAP")

map_data = pd.DataFrame({
    "lat": [28.6, 40.7, 51.5, 35.6, -33.8],
    "lon": [77.2, -74.0, -0.1, 139.6, 151.2],
    "size": [100, 80, 60, 90, 70],
    "attack": ["DDoS", "Scan", "Bruteforce", "SQLi", "Botnet"]
})

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    get_position='[lon, lat]',
    get_radius="size",
    get_color=[255, 0, 0],
    pickable=True
)

view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1.2
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{attack}"}
))