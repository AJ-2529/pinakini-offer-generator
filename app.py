import streamlit as st
from docxtpl import DocxTemplate
import datetime
import pandas as pd
import pydeck as pdk
import json

st.set_page_config(page_title="Pinakini Infra", layout="centered")

# -----------------------------
# MAP SETTINGS (EDITABLE)
# -----------------------------

MAP_HEIGHT = 650
MAP_ZOOM = 3.6
DOT_SIZE = 28000

# -----------------------------
# SESSION STATES
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "section" not in st.session_state:
    st.session_state.section = "offer_dashboard"

# -----------------------------
# CSS
# -----------------------------

st.markdown("""
<style>

body {
    background-color:#0e1117;
}

.title {
    font-size:52px;
    font-weight:700;
    text-align:center;
}

.white { color:white; }
.red { color:#ff4b4b; }

.login-text{
    font-size:30px;
    text-align:center;
    margin-bottom:20px;
}

.dashboard-title{
    font-size:34px;
    font-weight:600;
    margin-bottom:50px;
}

.sidebar-title{
    font-size:22px;
    font-weight:700;
    margin-bottom:20px;
}

.sidebar-section{
    font-size:12px;
    letter-spacing:1px;
    margin-top:25px;
    margin-bottom:10px;
    color:#9aa0a6;
}

.map-title{
    text-align:center;
    font-size:32px;
    font-weight:600;
    margin-bottom:20px;
}

.legend-fixed{
    position:fixed;
    bottom:40px;
    right:40px;
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# USERS
# -----------------------------

users = dict(st.secrets["users"])

# -----------------------------
# LOGIN
# -----------------------------

if not st.session_state.logged_in:

    st.markdown("""
    <div class="title">
    <span class="white">Pinakini</span>
    <span class="red">Infra</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='white login-text'>Login</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in users and users[username] == password:

            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()

        else:
            st.error("Invalid username or password")

    st.stop()

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.markdown('<div class="sidebar-title">Pinakini Infra</div>', unsafe_allow_html=True)

    if st.button("Dashboard"):
        st.session_state.section = "dashboard"
        st.rerun()

    st.markdown('<div class="sidebar-section">OFFERS</div>', unsafe_allow_html=True)

    if st.button("Offer Dashboard"):
        st.session_state.section = "offer_dashboard"
        st.rerun()

    if st.button("Offer History"):
        st.session_state.section = "history"
        st.rerun()

    st.markdown('<div class="sidebar-section">SITES</div>', unsafe_allow_html=True)

    if st.button("Sites"):
        st.session_state.section = "sites"
        st.rerun()

# -----------------------------
# DASHBOARD
# -----------------------------

if st.session_state.section == "dashboard":

    st.markdown(f"""
    <div class="dashboard-title">
    <span class="white">Welcome </span>
    <span class="red">{st.session_state.user}</span>
    </div>
    """, unsafe_allow_html=True)

    st.info("Dashboard module coming soon.")

# -----------------------------
# OFFERS DASHBOARD
# -----------------------------

elif st.session_state.section == "offer_dashboard":

    st.markdown("""
    <div class="dashboard-title">
    <span class="white">Create Offer</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Piling Rig"):
            st.session_state.section = "piling"
            st.rerun()

    with col2:
        if st.button("Shotcrete"):
            st.session_state.section = "shotcrete"
            st.rerun()

    with col3:
        if st.button("Stationery Boom Placer"):
            st.session_state.section = "boom"
            st.rerun()

# -----------------------------
# PILING RIG
# -----------------------------

elif st.session_state.section == "piling":

    if st.button("← Back to Offers"):
        st.session_state.section = "offer_dashboard"
        st.rerun()

    st.title("Piling Rig Offer Generator")
    st.info("Coming Soon")

# -----------------------------
# SHOTCRETE
# -----------------------------

elif st.session_state.section == "shotcrete":

    if st.button("← Back to Offers"):
        st.session_state.section = "offer_dashboard"
        st.rerun()

    st.title("Shotcrete Offer Generator")
    st.info("Coming Soon")

# -----------------------------
# BOOM PLACER GENERATOR
# -----------------------------

elif st.session_state.section == "boom":

    if st.button("← Back to Offers"):
        st.session_state.section = "offer_dashboard"
        st.rerun()

    st.title("Stationery Boom Placer Offer Generator")

    date = st.date_input("Date")
    address = st.text_area("To Address")
    gstn = st.text_input("GSTN")
    contact = st.text_input("Contact")
    email = st.text_input("Email")
    quantity = st.number_input("Number of Boom Placers", min_value=1)
    location = st.text_input("Location")
    rate = st.text_input("Monthly Rate (INR)")

    def indian_format(num):
        try:
            num = int(num)
        except:
            return num

        s = str(num)

        if len(s) <= 3:
            return s

        last3 = s[-3:]
        rest = s[:-3]

        parts = []

        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]

        if rest:
            parts.insert(0, rest)

        return ",".join(parts) + "," + last3

    if st.button("Generate Offer Letter"):

        template = DocxTemplate("templates/offer_template.docx")

        formatted_rate = indian_format(rate)

        context = {
            "date": date.strftime("%d/%m/%Y"),
            "address": address,
            "gstn": gstn,
            "contact": contact,
            "email": email,
            "quantity": quantity,
            "location": location,
            "rate": formatted_rate
        }

        template.render(context)

        filename = "offer_letter.docx"

        template.save(filename)

        with open(filename, "rb") as f:

            st.download_button(
                label="Download Offer Letter",
                data=f,
                file_name="offer_letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

# -----------------------------
# SITES MAP
# -----------------------------

elif st.session_state.section == "sites":

    st.markdown("""
    <div class="map-title">
    <span class="white">Pinakini Infra </span>
    <span class="red">Sites</span>
    </div>
    """, unsafe_allow_html=True)

    data = pd.read_csv("sites.csv")

    with open("countries.geojson") as f:
        world = json.load(f)

    india_geo = {
        "type": "FeatureCollection",
        "features": [
            feature for feature in world["features"]
            if feature["properties"].get("name") == "India"
        ],
    }

    india_layer = pdk.Layer(
        "GeoJsonLayer",
        india_geo,
        stroked=True,
        filled=False,
        get_line_color=[255,255,255],
        line_width_min_pixels=2,
    )

    data["color"] = data["status"].apply(
        lambda x: [255,0,0] if x=="working" else [0,255,0]
    )

    sites_layer = pdk.Layer(
        "ScatterplotLayer",
        data,
        get_position="[longitude, latitude]",
        get_color="color",
        get_radius=DOT_SIZE,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=22.5937,
        longitude=78.9629,
        zoom=MAP_ZOOM,
    )

    deck = pdk.Deck(
        layers=[india_layer, sites_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={
            "html": """
            <b>{site}</b><br/>
            Client: {client}<br/>
            Equipment: {equipment}<br/>
            Year: {year}<br/>
            Status: {status}
            """
        }
    )

    st.pydeck_chart(deck, height=MAP_HEIGHT)

    st.markdown("""
    <div class="legend-fixed">
    🔴 Working Site<br>
    🟢 Completed Site
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# OFFER HISTORY
# -----------------------------

elif st.session_state.section == "history":

    st.title("Offer History")
    st.info("Offer history will appear here later.")