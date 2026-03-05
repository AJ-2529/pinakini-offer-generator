import streamlit as st
from docxtpl import DocxTemplate
import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(page_title="Pinakini Infra", layout="centered")

# -----------------------------
# SESSION STATES
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# -----------------------------
# CUSTOM CSS
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

.white {
    color:white;
}

.red {
    color:#ff4b4b;
}

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

/* BIG EQUIPMENT CARDS */

.card button{
    background-color:#1f1f1f;
    color:white;
    border:1px solid #2a2a2a;
    padding:70px 40px;
    border-radius:18px;
    font-size:24px;
    font-weight:600;
    width:100%;
    height:200px;
    transition:all 0.25s ease;
}

.card button:hover{
    transform:translateY(-10px);
    border:1px solid #ff4b4b;
    box-shadow:0px 12px 35px rgba(0,0,0,0.6);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# USERS FROM STREAMLIT SECRETS
# -----------------------------

users = dict(st.secrets["users"])

# -----------------------------
# LOGIN PAGE
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
# DASHBOARD
# -----------------------------

if st.session_state.page == "dashboard":

    st.markdown(f"""
    <div class="dashboard-title">
    <span class="white">Welcome </span>
    <span class="red">{st.session_state.user}</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Piling Rig"):
            st.session_state.page = "piling"
            st.rerun()

    with col2:
        if st.button("Shotcrete"):
            st.session_state.page = "shotcrete"
            st.rerun()

    with col3:
        if st.button("Stationery Boom Placer"):
            st.session_state.page = "boom"
            st.rerun()

# -----------------------------
# PILING RIG PAGE
# -----------------------------

elif st.session_state.page == "piling":

    if st.button("← Back"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.title("Piling Rig Offer Generator")
    st.info("Equipment Offer Generator Coming Soon")

# -----------------------------
# SHOTCRETE PAGE
# -----------------------------

elif st.session_state.page == "shotcrete":

    if st.button("← Back"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.title("Shotcrete Offer Generator")
    st.info("Equipment Offer Generator Coming Soon")

# -----------------------------
# BOOM PLACER GENERATOR
# -----------------------------

elif st.session_state.page == "boom":

    if st.button("← Back"):
        st.session_state.page = "dashboard"
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

    # -----------------------------
    # INDIAN NUMBER FORMAT
    # -----------------------------

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

    # -----------------------------
    # GENERATE OFFER LETTER
    # -----------------------------

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

        st.success("Offer Letter Generated Successfully!")