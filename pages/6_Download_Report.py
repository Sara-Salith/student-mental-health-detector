import streamlit as st


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Download Report | MindAura AI",
    page_icon="📄",
    layout="centered"
)


# --------------------------------------------------
# CHECK LOGIN
# --------------------------------------------------

if not st.session_state.get("logged_in", False):

    st.warning("Please login first.")

    st.stop()


# --------------------------------------------------
# CHECK RESULT
# --------------------------------------------------

if (
    "assessment_data" not in st.session_state
    or "prediction" not in st.session_state
):

    st.warning("No assessment result found.")

    st.stop()


# --------------------------------------------------
# GET DATA
# --------------------------------------------------

username = st.session_state.get("username", "Student")

prediction = st.session_state.get(
    "prediction",
    "Not Available"
)

risk_score = st.session_state.get(
    "risk_score",
    0
)

ai_result = st.session_state.get(
    "ai_result",
    "AI wellness analysis is not available."
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📄 Mental Health Assessment Report")

st.write(
    f"Your complete wellness assessment report, **{username}**."
)

st.divider()


# --------------------------------------------------
# REPORT PREVIEW
# --------------------------------------------------

st.subheader("📊 Screening Result")

st.write(
    f"**Prediction:** {prediction}"
)

st.write(
    f"**Estimated Risk Score:** {risk_score:.1f}%"
)

st.caption(
    "This score is an AI-based screening estimate "
    "and is not a medical diagnosis."
)


st.divider()


# --------------------------------------------------
# AI ANALYSIS
# --------------------------------------------------

st.subheader("🤖 Personalized Wellness Analysis")

st.write(ai_result)


st.divider()


# --------------------------------------------------
# COMPLETE REPORT TEXT
# --------------------------------------------------

report_text = f"""
==================================================
             MINDAURA AI
      STUDENT MENTAL HEALTH ASSESSMENT REPORT
==================================================

Student Name / Username:
{username}

==================================================
SCREENING RESULT
==================================================

Prediction:
{prediction}

Estimated Mental Health Risk Score:
{risk_score:.1f}%

IMPORTANT:
This score is an AI-based screening estimate and
is not a medical or clinical diagnosis.

==================================================
PERSONALIZED WELLNESS ANALYSIS
==================================================

{ai_result}

==================================================
DISCLAIMER
==================================================

This application is designed for educational and
mental health screening purposes only.

It does not replace professional mental health
evaluation, medical diagnosis, treatment, or advice.

If you are experiencing serious emotional distress
or feel unsafe, please consider contacting a
qualified mental health professional or local
emergency support service.

==================================================
                 MINDAURA AI
==================================================
"""


# --------------------------------------------------
# DOWNLOAD BUTTON
# --------------------------------------------------

st.divider()

st.download_button(
    label="📥 Download Complete Report",
    data=report_text,
    file_name="MindAura_Mental_Health_Report.txt",
    mime="text/plain",
    use_container_width=True
)