import streamlit as st
from ai_helper import get_ai_analysis
from components.navigation import (
    login_page,
    assessment_page
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1500px !important;
        width: 100% !important;
        padding-top: 1rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        padding-bottom: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Result | Student Mental Health Detector",
    page_icon="🧠",
    layout="centered"
)


# --------------------------------------------------
# CHECK LOGIN
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("Please login first.")

    if st.button("Go to Login"):
        st.switch_page(login_page)

    st.stop()


# --------------------------------------------------
# CHECK ASSESSMENT DATA
# --------------------------------------------------

if "assessment_data" not in st.session_state or "prediction" not in st.session_state:

    st.warning("No assessment result found.")

    if st.button("Take Assessment"):
        st.switch_page(assessment_page)

    st.stop()


# --------------------------------------------------
# GET DATA
# --------------------------------------------------

student_data = st.session_state.assessment_data
prediction = st.session_state.prediction


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <h1 style="text-align:center;">
        🧠 Your Mental Health Result
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <p style="text-align:center;color:#666;">
        Assessment result for <b>{st.session_state.username}</b>
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# ML RESULT
# --------------------------------------------------

st.subheader("📊 Screening Result")

if prediction == "Higher Mental Health Risk":

    st.error(
        "⚠️ Higher Mental Health Risk Detected"
    )

    st.write(
        "The machine learning model has identified a higher "
        "predicted risk based on the responses provided."
    )

else:

    st.success(
        "✅ Lower Mental Health Risk"
    )

    st.write(
        "The machine learning model has identified a lower "
        "predicted risk based on the responses provided."
    )


st.info(
    "This result is an AI-based screening prediction and "
    "is not a medical diagnosis."
)


# --------------------------------------------------
# GEMINI AI ANALYSIS
# --------------------------------------------------

st.divider()

st.subheader("🤖 AI Wellness Analysis")

with st.spinner("Gemini AI is analyzing your responses..."):

    try:

        ai_result = get_ai_analysis(
            student_data,
            prediction
        )

        st.write(ai_result)

    except Exception as e:

        st.error(
            "The AI analysis could not be generated."
        )

        st.code(str(e))


# --------------------------------------------------
# WELLNESS DISCLAIMER
# --------------------------------------------------

st.divider()

st.caption(
    "🧠 This application is intended for educational and "
    "screening purposes only. It does not replace professional "
    "mental-health evaluation or medical advice."
)


# --------------------------------------------------
# NAVIGATION BUTTONS
# --------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🔄 Take Assessment Again",
        use_container_width=True
    ):

        # Remove old result
        st.session_state.pop("assessment_data", None)
        st.session_state.pop("prediction", None)

        st.switch_page(assessment_page)


with col2:

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        # Clear login information
        st.session_state.logged_in = False
        st.session_state.username = ""

        # Clear assessment information
        st.session_state.pop("assessment_data", None)
        st.session_state.pop("prediction", None)

        st.switch_page(login_page)