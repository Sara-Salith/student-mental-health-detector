import streamlit as st

from components.navigation import (
    login_page,
    dashboard_page,
    assessment_page,
    result_page,
    history_page,
    download_report_page
)
from mind_aura_chatbot import render_mind_aura_chatbot

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Student Mental Health Detector",
    page_icon="🧠",
    layout="wide"
)

# ==================================================
# MOBILE RESPONSIVE STYLING
# ==================================================

st.markdown("""
<style>

/* Improve spacing on mobile screens */
@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
    }

    /* Make headings fit smaller screens */
    h1 {
        font-size: 1.7rem !important;
        line-height: 1.3 !important;
    }

    h2 {
        font-size: 1.4rem !important;
    }

    h3 {
        font-size: 1.15rem !important;
    }

    /* Keep buttons easy to tap */
    .stButton > button,
    .stFormSubmitButton > button {
        width: 100%;
        min-height: 44px;
    }

    /* Make input fields easier to use */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox,
    .stTextArea textarea {
        font-size: 16px !important;
    }

    /* Prevent tables from forcing a wide layout */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        max-width: 100%;
        overflow-x: auto;
    }

    /* Improve chat readability */
    [data-testid="stChatMessage"] {
        padding: 0.75rem !important;
    }
}

</style>
""", unsafe_allow_html=True)


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

games_page = st.Page(
    "pages/7_Wellness_Games.py",
    title="Wellness Games",
    url_path="wellness-games",
    icon="🎮"
)

memory_match_page = st.Page(
    "pages/8_Memory_Match.py",
    title="Memory Match",
    url_path="memory-match",
    icon="🧠"
)

breathing_page = st.Page(
    "pages/9_Breathing_Challenge.py",
    title="Breathing Challenge",
    url_path="breathing-challenge",
    icon="🌬️"
)

mood_garden_page = st.Page(
    "pages/10_Mood_Garden.py",
    title="Mood Garden",
    url_path="mood-garden",
    icon="🌷"
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
            history_page,
            games_page,
            memory_match_page,
            breathing_page,
            mood_garden_page,
            download_report_page
        ],
        position="hidden"
    )

else:

    pg = st.navigation(
        [login_page],
        position="hidden"
    )

if st.session_state.logged_in:
    render_mind_aura_chatbot()
pg.run()