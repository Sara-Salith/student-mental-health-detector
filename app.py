import streamlit as st

from components.navigation import (
    login_page,
    dashboard_page,
    assessment_page,
    result_page,
    history_page
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Student Mental Health Detector",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# SESSION STATE
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# ==================================================
# PAGE DEFINITIONS
# ==================================================

login_page = st.Page(
    "pages/1_Login_Register.py",
    title="Login / Register",
    url_path="login",
    icon="🔐"
)

dashboard_page = st.Page(
    "pages/2_Dashboard.py",
    title="Dashboard",
    url_path="dashboard",
    icon="🏠"
)

assessment_page = st.Page(
    "pages/3_Assessment.py",
    title="Assessment",
    url_path="assessment",
    icon="🧠"
)

result_page = st.Page(
    "pages/4_Result.py",
    title="Result",
    url_path="result",
    icon="📊"
)

history_page = st.Page(
    "pages/5_History.py",
    title="History",
    url_path="history",
    icon="📋"
)


# ==================================================
# NAVIGATION
# ==================================================

if st.session_state.logged_in:

    pg = st.navigation(
        [
            dashboard_page,
            assessment_page,
            result_page,
            history_page
        ],
        position="hidden"
    )

else:

    pg = st.navigation(
        [login_page],
        position="hidden"
    )

pg.run()