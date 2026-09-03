import streamlit as st
import plotly.graph_objects as go

from ai_helper import get_ai_analysis
from components.navigation import (
    assessment_page,
    login_page,
    dashboard_page,
    download_report_page
)


# ==================================================
# PAGE CONFIG - MUST BE FIRST STREAMLIT COMMAND
# ==================================================

st.set_page_config(
    page_title="Result | Student Mental Health Detector",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #f6f8fc;
}


/* Main page width */

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    padding-bottom: 3rem;
}


/* Hide Streamlit default header */

header {
    visibility: hidden;
}


/* Main title */

.result-title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    color: #263248;
    margin-bottom: 0px;
}


.result-subtitle {
    text-align: center;
    font-size: 16px;
    color: #667085;
    margin-bottom: 20px;
}


/* Section headings */

.section-heading {
    font-size: 23px;
    font-weight: 700;
    color: #263248;
}


/* Cards */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px;
}


/* Risk guide */

.risk-guide {
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 12px;
    font-size: 15px;
}


.low-risk {
    background-color: #eaf8f0;
}


.moderate-risk {
    background-color: #fff7df;
}


.high-risk {
    background-color: #fff0f0;
}


.guide-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 15px;
    color: #374151;
}


/* Meaning card */

.meaning-card {
    background: #fafafa;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    margin-top: 16px;
}


/* Disclaimer */

.disclaimer {
    color: #6b7280;
    font-size: 14px;
    font-style: italic;
}


/* Buttons */

.stButton button {
    border-radius: 8px;
    font-weight: 600;
    min-height: 45px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# CHECK LOGIN
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.warning("Please login first.")

    if st.button("Go to Login"):
        st.switch_page(login_page)

    st.stop()


# ==================================================
# CHECK ASSESSMENT DATA
# ==================================================

if (
    "assessment_data" not in st.session_state
    or "prediction" not in st.session_state
):

    st.warning("No assessment result found.")

    if st.button("Take Assessment"):
        st.switch_page(assessment_page)

    st.stop()


# ==================================================
# GET DATA
# ==================================================

student_data = st.session_state.assessment_data

prediction = st.session_state.prediction

risk_score = float(
    st.session_state.get("risk_score", 0.0)
)

username = st.session_state.get(
    "username",
    "Student"
)


# ==================================================
# DETERMINE RISK LEVEL
# ==================================================

if risk_score <= 33:

    risk_level = "Low Risk"
    risk_color = "#15803d"

elif risk_score <= 66:

    risk_level = "Moderate Risk"
    risk_color = "#d97706"

else:

    risk_level = "High Risk"
    risk_color = "#dc2626"


# ==================================================
# TOP NAVIGATION
# ==================================================

nav1, nav2, nav3, nav4 = st.columns(
    [1.2, 3, 1.3, 1.8]
)


with nav1:
    if st.button(
        "← Back",
        key="top_back_button",
        width="stretch"
    ):
        st.switch_page(assessment_page)


with nav3:
    if st.button(
        "🏠 Dashboard",
        key="top_dashboard_button",
        width="stretch"
    ):
        st.switch_page(dashboard_page)


with nav4:
    if st.button(
        "🔄 Take Assessment Again",
        key="top_assessment_again_button",
        width="stretch"
    ):
        st.session_state.assessment_step = 1
        st.session_state.new_assessment = True

        st.session_state.pop("assessment_data", None)
        st.session_state.pop("prediction", None)
        st.session_state.pop("risk_score", None)
        st.session_state.pop("ai_result", None)

        st.switch_page(assessment_page)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    f"""
    <div class="result-title">
        🧠 Your Mental Health Result
    </div>

    <div class="result-subtitle">
        Assessment result for <b>{username}</b>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SCREENING RESULT
# ==================================================

with st.container(border=True):

    st.markdown(
        '<p class="section-heading">🎯 Screening Result</p>',
        unsafe_allow_html=True
    )

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
            "✅ Lower Mental Health Risk Detected"
        )

        st.write(
            "The machine learning model has identified a lower "
            "predicted risk based on the responses provided."
        )


    st.info(
        "ℹ️ This result is an AI-based screening prediction "
        "and is not a medical diagnosis."
    )


# ==================================================
# RISK SCORE
# ==================================================

st.write("")

with st.container(border=True):

    st.markdown(
        '<p class="section-heading">📊 Your Risk Score</p>',
        unsafe_allow_html=True
    )

    left_col, right_col = st.columns(
        [1, 1.1],
        gap="large"
    )


    # ==============================================
    # LEFT SIDE - GAUGE
    # ==============================================

    with left_col:

        fig = go.Figure(
            go.Indicator(

                mode="gauge+number",

                value=risk_score,

                number={
                    "suffix": "%",
                    "font": {
                        "size": 55,
                        "color": risk_color
                    }
                },

                gauge={

                    "axis": {
                        "range": [0, 100]
                    },

                    "bar": {
                        "color": "rgba(0,0,0,0)"
                    },

                    "steps": [

                        {
                            "range": [0, 33],
                            "color": "#22c55e"
                        },

                        {
                            "range": [33, 66],
                            "color": "#facc15"
                        },

                        {
                            "range": [66, 100],
                            "color": "#ef4444"
                        }

                    ],

                    "threshold": {

                        "line": {
                            "color": "#1f2937",
                            "width": 7
                        },

                        "thickness": 0.8,

                        "value": risk_score

                    }

                }

            )
        )


        fig.update_layout(

            height=340,

            margin=dict(
                l=20,
                r=20,
                t=30,
                b=0
            ),

            paper_bgcolor="rgba(0,0,0,0)",

            font={
                "color": "#374151"
            }

        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        st.markdown(
            f"""
            <h3 style="
                text-align:center;
                color:{risk_color};
                margin-top:-25px;
            ">
                {risk_level}
            </h3>
            """,
            unsafe_allow_html=True
        )


    # ==============================================
    # RIGHT SIDE - RISK GUIDE
    # ==============================================

    with right_col:

        st.subheader("Risk Level Guide")

        with st.container(border=True):

            st.markdown(
                """
                🟢 **0% - 33% — Low Risk**

                Your mental health risk is low.  
                Keep maintaining a healthy lifestyle!
                """
            )


        with st.container(border=True):

            st.markdown(
                """
                🟡 **34% - 66% — Moderate Risk**

                Your risk is moderate.  
                Try to manage stress and maintain balance.
                """
            )


        with st.container(border=True):

            st.markdown(
                """
                🔴 **67% - 100% — High Risk**

                Your risk is high.  
                Consider taking steps to improve your well-being.
                """
            )


        st.write("")


        with st.container(border=True):

            st.markdown("### ✨ What does this mean?")

            st.write(
                "The risk score is an AI-based estimate "
                "calculated from your responses."
            )

            st.write(
                "This is not a medical diagnosis. "
                "Please consult a qualified professional "
                "if you are experiencing distress."
            )
# ==================================================
# AI WELLNESS ANALYSIS
# ==================================================

st.write("")

with st.container(border=True):

    st.markdown("## 🤖 AI Wellness Analysis")

    st.caption(
        "This tool provides an AI-based screening result for wellness "
        "purposes and is not a medical diagnosis or clinical assessment. "
        "Mental health is dynamic, and results are based on a snapshot "
        "of self-reported data."
    )

    st.divider()

    # --------------------------------------------------
    # GENERATE AI ANALYSIS
    # --------------------------------------------------

    if "ai_result" not in st.session_state:

        with st.spinner(
            "🤖 AI is analyzing your responses..."
        ):

            try:

                result = get_ai_analysis(
                    student_data,
                    prediction
                )

                # Only save the result if Gemini actually
                # returned useful content
                if result and str(result).strip():

                    st.session_state.ai_result = result

                else:

                    st.session_state.ai_result = None

            except Exception as e:

                st.session_state.ai_result = None

                st.session_state.ai_error = str(e)


    # --------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------

    if st.session_state.get("ai_result"):

        st.markdown(
            st.session_state.ai_result
        )

    else:

        st.warning(
            "⚠️ AI wellness analysis could not be generated "
            "right now. This may be a temporary AI service issue."
        )

        if st.button(
            "🔄 Retry AI Analysis",
            use_container_width=False
        ):

            st.session_state.pop(
                "ai_result",
                None
            )

            st.session_state.pop(
                "ai_error",
                None
            )

            st.rerun()


    st.divider()


    st.markdown(
        """
        <div class="disclaimer">

        <b>Disclaimer:</b>

        This tool provides an AI-based screening result
        for wellness purposes and is not a medical diagnosis
        or clinical assessment. Mental health is dynamic,
        and results are based on a snapshot of self-reported data.

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# BOTTOM NAVIGATION
# ==================================================

st.write("")
st.write("")


col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "🏠 Dashboard",
        key="bottom_dashboard_button",
        width="stretch"
    ):
        st.switch_page(dashboard_page)


with col2:

    if st.button(
        "📄 Download Report",
        key="download_report_button",
        width="stretch"
    ):
        st.switch_page(download_report_page)


with col3:

    if st.button(
        "🚪 Logout",
        key="logout_button",
        width="stretch"
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.session_state.pop("assessment_data", None)
        st.session_state.pop("prediction", None)
        st.session_state.pop("risk_score", None)
        st.session_state.pop("ai_result", None)

        st.switch_page(login_page)