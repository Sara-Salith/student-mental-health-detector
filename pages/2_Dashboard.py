import streamlit as st
import pandas as pd

from components.history import get_user_history
from components.navigation import (
    login_page,
    assessment_page,
    history_page,
    back_button
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Dashboard | MindAura",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# LOGIN CHECK
# ==================================================

if not st.session_state.get("logged_in", False):

    st.warning("Please login first.")
    st.stop()


username = st.session_state.username
back_button(login_page, "back_to_login")


# ==================================================
# LOAD HISTORY
# ==================================================

history = get_user_history(username)


# ==================================================
# CALCULATE STATISTICS
# ==================================================

if history.empty:

    total_tests = 0
    lower_risk = 0
    higher_risk = 0
    average_risk = 0

else:

    total_tests = len(history)

    higher_risk = len(
        history[
            history["prediction"] ==
            "Higher Mental Health Risk"
        ]
    )

    lower_risk = total_tests - higher_risk

    average_risk = history["risk_score"].mean()


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ============================================
       GLOBAL
       ============================================ */

    .stApp {
        background: #ffffff;
    }

    .block-container {
        max-width: 1500px !important;
        width: 100% !important;
        padding-top: 4rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        padding-bottom: 3rem !important;
    }

    /* ==================================================
   FIX TOP NAVIGATION VISIBILITY
   ================================================== */

   .top-nav {
       position: relative !important;
       top: 0 !important;
       left: 0 !important;
       right: auto !important;
       transform: none !important;

       width: 100% !important;
       min-height: 60px !important;

       display: flex !important;
       align-items: center !important;
       justify-content: space-between !important;

       margin-top: 0 !important;
       margin-bottom: 30px !important;
       padding: 12px 0 !important;

       visibility: visible !important;
       opacity: 1 !important;
       z-index: 1000 !important;

       overflow: visible !important;
   }

   .nav-left,
   .nav-center,
   .nav-right {
       position: relative !important;
       display: flex !important;
       align-items: center !important;
       visibility: visible !important;
       opacity: 1 !important;
   }

   .nav-center {
       gap: 12px !important;
   }

   .nav-right {
       gap: 10px !important;
   }

   .nav-item {
       position: relative !important;
       display: flex !important;
       align-items: center !important;
       justify-content: center !important;

       visibility: visible !important;
       opacity: 1 !important;

       color: #17203a !important;
       background: #ffffff !important;

       font-size: 14px !important;
       font-weight: 600 !important;

       padding: 9px 16px !important;
       border-radius: 10px !important;

       white-space: nowrap !important;
       z-index: 1001 !important;
   }

   .nav-active {
       background: #fce8f2 !important;
       color: #e83e8c !important;
   }

   .brand {
       position: relative !important;
       visibility: visible !important;
       opacity: 1 !important;

       color: #17203a !important;
       font-size: 22px !important;
       font-weight: 800 !important;
   }

    /* ============================================
       WELCOME
       ============================================ */

    .welcome-title {
        font-size: 34px;
        font-weight: 800;
        color: #20243a;
        margin-bottom: 4px;
    }

    .welcome-text {
        color: #687087;
        font-size: 15px;
        margin-bottom: 18px;
    }

    /* ============================================
       STAT CARDS
       ============================================ */

    .stat-card {
        background: #ffffff;
        border: 1px solid #e7e9f0;
        border-radius: 16px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 4px 15px rgba(32, 36, 58, 0.06);
    }

    .stat-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
        margin-bottom: 10px;
    }

    .blue-icon {
        background: #e7f0ff;
    }

    .green-icon {
        background: #e8f9ed;
    }

    .red-icon {
        background: #ffe9eb;
    }

    .purple-icon {
        background: #f2eaff;
    }

    .stat-number {
        font-size: 28px;
        font-weight: 800;
        color: #20243a;
    }

    .stat-label {
        font-size: 14px;
        font-weight: 700;
        color: #30364d;
        margin-top: 2px;
    }

    .stat-description {
        font-size: 12px;
        color: #7a8194;
        margin-top: 5px;
    }

    .green-number {
        color: #159447;
    }

    .red-number {
        color: #e53935;
    }

    .purple-number {
        color: #7c3aed;
    }

    /* ============================================
       SECTION TITLES
       ============================================ */

    .section-title {
        font-size: 21px;
        font-weight: 800;
        color: #20243a;
        margin-bottom: 12px;
    }

    /* ============================================
       TREND CARD
       ============================================ */

    .trend-card {
        background: #ffffff;
        border: 1px solid #e7e9f0;
        border-radius: 17px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(32, 36, 58, 0.05);
    }

    .trend-note {
        background: #eef6ff;
        color: #3178c6;
        border-radius: 10px;
        padding: 11px 14px;
        font-size: 13px;
        margin-top: 10px;
    }

    /* ============================================
       QUICK ACTION CARDS
       ============================================ */

    .action-card {
        background: #ffffff;
        border-radius: 15px;
        padding: 17px;
        border: 1px solid #e3e7ef;
        min-height: 110px;
        box-shadow: 0 3px 12px rgba(32, 36, 58, 0.04);
    }

    .action-blue {
        background: #f2f8ff;
        border-color: #c8e3ff;
    }

    .action-green {
        background: #f0fbf4;
        border-color: #c8ecd3;
    }

    .action-yellow {
        background: #fffaf0;
        border-color: #f6dfaa;
    }

    .action-title {
        font-size: 16px;
        font-weight: 800;
        color: #20243a;
    }

    .action-text {
        font-size: 12px;
        color: #667085;
        margin-top: 6px;
        line-height: 1.5;
    }

    /* ============================================
       WELLNESS CARDS
       ============================================ */

    .tip-card {
        background: #f4f8ff;
        border-radius: 13px;
        padding: 17px;
        min-height: 105px;
        border: 1px solid #e0e9f8;
    }

    .tip-title {
        font-size: 15px;
        font-weight: 800;
        color: #2868bd;
    }

    .tip-text {
        color: #667085;
        font-size: 12px;
        line-height: 1.5;
        margin-top: 5px;
    }

    /* ============================================
       RECENT ASSESSMENT
       ============================================ */

    .recent-card {
        background: #ffffff;
        border: 1px solid #e4e7ee;
        border-radius: 15px;
        box-shadow: 0 3px 12px rgba(32, 36, 58, 0.05);
        overflow: hidden;
    }

    .recent-row {
        padding: 13px 16px;
        border-bottom: 1px solid #eeeeee;
        display: flex;
        justify-content: space-between;
        color: #30364d;
        font-size: 13px;
    }

    .recent-label {
        font-weight: 700;
    }

    .risk-high {
        color: #e53935;
        font-weight: 800;
    }

    .risk-low {
        color: #159447;
        font-weight: 800;
    }

    /* ============================================
       DISCLAIMER
       ============================================ */

    .disclaimer {
        background: #eef6ff;
        border: 1px solid #cce2ff;
        color: #3276bd;
        padding: 12px 16px;
        border-radius: 10px;
        font-size: 12px;
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# HTML RENDER HELPER
# ==================================================

def render_html(content):
    st.html(content)


# ==================================================
# TOP NAVIGATION
# ==================================================

nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(
    [2.4, 1, 1, 1.2, 1.1, 0.8]
)


with nav1:

    render_html(
        """
        <div class="brand">
            🧠 Mind<span>Aura</span>
        </div>
        """
    )


with nav2:

    render_html(
        '<div class="nav-pill">Dashboard</div>'
    )


with nav3:

    if st.button(
        "Assessment",
        use_container_width=True,
        key="nav_assessment"
    ):
        st.switch_page(assessment_page)


with nav4:

    if st.button(
        "History",
        use_container_width=True,
        key="nav_history"
    ):
        st.switch_page(history_page)


with nav5:

    st.button(
        "💡 Wellness",
        use_container_width=True,
        key="nav_wellness"
    )


with nav6:

    if st.button(
        "Logout",
        use_container_width=True,
        key="nav_logout"
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""

        from components.navigation import login_page

        st.switch_page(login_page)


# ==================================================
# WELCOME SECTION
# ==================================================

render_html(
    f"""
    <div class="welcome-title">
        Hi, {username}! 👋
    </div>

    <div class="welcome-text">
        Track your mental wellness and understand your recent assessment trends.
    </div>
    """
)


if st.button(
    "🧠  Start New Assessment",
    key="main_assessment",
    use_container_width=False
):

    st.switch_page(assessment_page)


# ==================================================
# STATISTICS
# ==================================================

st.write("")


col1, col2, col3, col4 = st.columns(4)


with col1:

    render_html(
        f"""
        <div class="stat-card">

            <div class="stat-icon blue-icon">
                📋
            </div>

            <div class="stat-number">
                {total_tests}
            </div>

            <div class="stat-label">
                Total Assessments
            </div>

            <div class="stat-description">
                All time assessments completed
            </div>

        </div>
        """
    )


with col2:

    render_html(
        f"""
        <div class="stat-card">

            <div class="stat-icon green-icon">
                ✓
            </div>

            <div class="stat-number green-number">
                {lower_risk}
            </div>

            <div class="stat-label">
                Lower Risk
            </div>

            <div class="stat-description">
                Assessments with low risk
            </div>

        </div>
        """
    )


with col3:

    render_html(
        f"""
        <div class="stat-card">

            <div class="stat-icon red-icon">
                !
            </div>

            <div class="stat-number red-number">
                {higher_risk}
            </div>

            <div class="stat-label">
                Higher Risk
            </div>

            <div class="stat-description">
                Assessments with high risk
            </div>

        </div>
        """
    )


with col4:

    render_html(
        f"""
        <div class="stat-card">

            <div class="stat-icon purple-icon">
                %
            </div>

            <div class="stat-number purple-number">
                {average_risk:.0f}%
            </div>

            <div class="stat-label">
                Average Risk Score
            </div>

            <div class="stat-description">
                Average of all your risk scores
            </div>

        </div>
        """
    )


# ==================================================
# MAIN DASHBOARD CONTENT
# ==================================================

left_col, right_col = st.columns([2.1, 1], gap="large")


# ==================================================
# LEFT COLUMN
# TREND + WELLNESS
# ==================================================

with left_col:

    # ----------------------------------------------
    # MENTAL HEALTH TREND
    # ----------------------------------------------

    render_html(
        '<div class="section-title">📈 Mental Health Trend</div>'
    )

    render_html(
        '<div class="trend-card">'
    )

    if history.empty:

        st.info(
            "Complete your first assessment to start tracking your mental health trend."
        )

    else:

        graph_data = history.copy()

        graph_data["timestamp"] = pd.to_datetime(
            graph_data["timestamp"]
        )

        graph_data = graph_data.sort_values(
            "timestamp"
        )

        graph_data = graph_data.set_index(
            "timestamp"
        )

        st.line_chart(
            graph_data["risk_score"],
            height=300
        )

        render_html(
            """
            <div class="trend-note">
                ℹ️ Keep taking assessments regularly to track your progress over time.
            </div>
            """
        )

    render_html(
        "</div>"
    )


    # ----------------------------------------------
    # TODAY'S WELLNESS TIPS
    # ----------------------------------------------

    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)

    render_html(
        '<div class="section-title">💡 Today\'s Wellness Tips</div>'
    )

    tip1, tip2, tip3 = st.columns(3, gap="medium")


    with tip1:

        render_html(
            """
            <div class="tip-card">

                <div class="tip-title">
                    😴 Aim for 7–8 hours of sleep
                </div>

                <div class="tip-text">
                    Quality sleep improves focus, mood and overall well-being.
                </div>

            </div>
            """
        )


    with tip2:

        render_html(
            """
            <div class="tip-card">

                <div class="tip-title">
                    🚶 Take short breaks
                </div>

                <div class="tip-text">
                    Step away from studying regularly to reduce stress and refresh your mind.
                </div>

            </div>
            """
        )


    with tip3:

        render_html(
            """
            <div class="tip-card">

                <div class="tip-title">
                    🧘 Try mindful breathing
                </div>

                <div class="tip-text">
                    Spend a few minutes focusing on slow, deep breathing.
                </div>

            </div>
            """
        )


# ==================================================
# RIGHT COLUMN
# QUICK ACTIONS + RECENT ASSESSMENT
# ==================================================

with right_col:

    # ----------------------------------------------
    # QUICK ACTIONS
    # ----------------------------------------------

    render_html(
        '<div class="section-title">⚡ Quick Actions</div>'
    )


    render_html(
        """
        <div class="action-card action-blue">

            <div class="action-title">
                🧠 Start Assessment
            </div>

            <div class="action-text">
                Take a new mental wellness assessment and get an updated AI-powered analysis.
            </div>

        </div>
        """
    )


    if st.button(
        "Start Assessment  →",
        key="action_assessment",
        use_container_width=True
    ):

        st.switch_page(assessment_page)


    st.write("")


    render_html(
        """
        <div class="action-card action-green">

            <div class="action-title">
                📊 View History
            </div>

            <div class="action-text">
                Review your previous assessments, results and risk scores.
            </div>

        </div>
        """
    )


    if st.button(
        "View History  →",
        key="action_history",
        use_container_width=True
    ):

        st.switch_page(history_page)


    st.write("")


    render_html(
        """
        <div class="action-card action-yellow">

            <div class="action-title">
                💡 Wellness Tips
            </div>

            <div class="action-text">
                Get personalized suggestions based on your recent mental wellness status.
            </div>

        </div>
        """
    )


    if st.button(
        "View Tips  →",
        key="action_tips",
        use_container_width=True
    ):

        st.info(
            "Complete an assessment to receive personalized AI wellness recommendations."
        )


    # ----------------------------------------------
    # RECENT ASSESSMENT
    # ----------------------------------------------

    st.markdown(
        "<div style='height:25px'></div>",
        unsafe_allow_html=True
    )

    render_html(
        '<div class="section-title">🕒 Recent Assessment</div>'
    )


    if history.empty:

        render_html(
            """
            <div class="recent-card">

                <div class="recent-row">
                    No assessment completed yet.
                </div>

            </div>
            """
        )

    else:

        latest = history.sort_values(
            "timestamp",
            ascending=False
        ).iloc[0]


        result_class = (
            "risk-high"
            if latest["prediction"] ==
            "Higher Mental Health Risk"
            else "risk-low"
        )


        render_html(
            f"""
            <div class="recent-card">

                <div class="recent-row">

                    <span class="recent-label">
                        📅 Date
                    </span>

                    <span>
                        {latest["timestamp"]}
                    </span>

                </div>


                <div class="recent-row">

                    <span class="recent-label">
                        🛡️ Result
                    </span>

                    <span class="{result_class}">
                        {latest["prediction"]}
                    </span>

                </div>


                <div class="recent-row">

                    <span class="recent-label">
                        📊 Risk Score
                    </span>

                    <span class="{result_class}">
                        {latest["risk_score"]:.0f}%
                    </span>

                </div>

            </div>
            """
        )