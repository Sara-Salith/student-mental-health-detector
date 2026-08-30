import streamlit as st
import pandas as pd

from components.history import get_user_history
from components.navigation import (
    login_page,
    dashboard_page,
    assessment_page,
    history_page,
    back_button
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Assessment History | MindAura",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# LOGIN CHECK
# ==================================================

if not st.session_state.get("logged_in", False):

    st.warning("Please login first.")

    if st.button("Go to Login"):
        st.switch_page(login_page)

    st.stop()


username = st.session_state.username


# ==================================================
# BACK BUTTON
# ==================================================

back_button(dashboard_page, "back_to_dashboard")


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1500px !important;
        padding-top: 3rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }

    .history-header {
        font-size: 34px;
        font-weight: 800;
        color: #20243a;
    }

    .history-subtitle {
        font-size: 15px;
        color: #687087;
        margin-bottom: 25px;
    }

    .summary-card {
        background: white;
        border: 1px solid #e4e7ee;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(32, 36, 58, 0.05);
        text-align: center;
    }

    .summary-number {
        font-size: 28px;
        font-weight: 800;
        color: #20243a;
    }

    .summary-label {
        font-size: 13px;
        color: #687087;
        margin-top: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    f"""
    <div class="history-header">
        🕒 Assessment History
    </div>

    <div class="history-subtitle">
        View your previous mental wellness assessments and track your progress over time, {username}.
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD HISTORY FROM SUPABASE
# ==================================================

history = get_user_history(username)


# ==================================================
# EMPTY HISTORY
# ==================================================

if history.empty:

    st.info(
        "You haven't completed any assessments yet."
    )

    st.write("")

    if st.button(
        "🧠 Take Your First Assessment",
        use_container_width=False
    ):
        st.switch_page(assessment_page)

    st.stop()


# ==================================================
# CONVERT TIMESTAMP
# ==================================================

history["timestamp"] = pd.to_datetime(
    history["timestamp"]
)

history = history.sort_values(
    "timestamp",
    ascending=False
)


# ==================================================
# SUMMARY STATISTICS
# ==================================================

total_assessments = len(history)

higher_risk = len(
    history[
        history["prediction"]
        == "Higher Mental Health Risk"
    ]
)

lower_risk = total_assessments - higher_risk

average_risk = history["risk_score"].mean()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📋 Total Assessments",
        total_assessments
    )


with col2:

    st.metric(
        "✅ Lower Risk",
        lower_risk
    )


with col3:

    st.metric(
        "⚠️ Higher Risk",
        higher_risk
    )


with col4:

    st.metric(
        "📊 Average Risk",
        f"{average_risk:.1f}%"
    )


st.write("")
st.divider()


# ==================================================
# RISK TREND
# ==================================================

st.subheader("📈 Mental Health Risk Trend")

chart_data = history.copy()

chart_data = chart_data.sort_values(
    "timestamp"
)

chart_data = chart_data.set_index(
    "timestamp"
)

st.line_chart(
    chart_data["risk_score"],
    height=300
)


st.divider()


# ==================================================
# ASSESSMENT HISTORY TABLE
# ==================================================

st.subheader("📋 Previous Assessments")


# Create a cleaner version for display
display_history = history[
    [
        "timestamp",
        "prediction",
        "risk_score",
        "gender",
        "age",
        "cgpa",
        "academic_pressure",
        "study_satisfaction",
        "sleep_duration",
        "dietary_habits",
        "financial_stress"
    ]
].copy()


# Format timestamp
display_history["timestamp"] = (
    display_history["timestamp"]
    .dt.strftime("%d %b %Y, %I:%M %p")
)


# Round risk score
display_history["risk_score"] = (
    display_history["risk_score"]
    .round(2)
)


# Rename columns for professional display
display_history = display_history.rename(
    columns={
        "timestamp": "Date & Time",
        "prediction": "Result",
        "risk_score": "Risk Score (%)",
        "gender": "Gender",
        "age": "Age",
        "cgpa": "CGPA",
        "academic_pressure": "Academic Pressure",
        "study_satisfaction": "Study Satisfaction",
        "sleep_duration": "Sleep Duration",
        "dietary_habits": "Dietary Habits",
        "financial_stress": "Financial Stress"
    }
)


st.dataframe(
    display_history,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# VIEW DETAILED ASSESSMENTS
# ==================================================

st.divider()

st.subheader("🔍 View Assessment Details")


assessment_options = []

for index, row in history.iterrows():

    date = row["timestamp"].strftime(
        "%d %b %Y, %I:%M %p"
    )

    assessment_options.append(
        f"{date} — {row['prediction']}"
    )


selected_assessment = st.selectbox(
    "Select an assessment",
    assessment_options
)


selected_index = assessment_options.index(
    selected_assessment
)

selected_record = history.iloc[selected_index]


st.write("")

col1, col2 = st.columns(2)


with col1:

    st.markdown("### 👤 Student Information")

    st.write(
        f"**Gender:** {selected_record.get('gender', 'N/A')}"
    )

    st.write(
        f"**Age:** {selected_record.get('age', 'N/A')}"
    )

    st.write(
        f"**CGPA:** {selected_record.get('cgpa', 'N/A')}"
    )

    st.write(
        f"**Sleep Duration:** {selected_record.get('sleep_duration', 'N/A')}"
    )

    st.write(
        f"**Dietary Habits:** {selected_record.get('dietary_habits', 'N/A')}"
    )


with col2:

    st.markdown("### 📊 Assessment Information")

    st.write(
        f"**Prediction:** {selected_record.get('prediction', 'N/A')}"
    )

    st.write(
        f"**Risk Score:** {selected_record.get('risk_score', 0):.2f}%"
    )

    st.write(
        f"**Academic Pressure:** "
        f"{selected_record.get('academic_pressure', 'N/A')}"
    )

    st.write(
        f"**Study Satisfaction:** "
        f"{selected_record.get('study_satisfaction', 'N/A')}"
    )

    st.write(
        f"**Financial Stress:** "
        f"{selected_record.get('financial_stress', 'N/A')}"
    )


st.divider()


# ==================================================
# BUTTONS
# ==================================================

col1, col2 = st.columns(2)


with col1:

    if st.button(
        "🧠 Take New Assessment",
        use_container_width=True
    ):

        st.switch_page(assessment_page)


with col2:

    if st.button(
        "🏠 Back to Dashboard",
        use_container_width=True
    ):

        st.switch_page(dashboard_page)