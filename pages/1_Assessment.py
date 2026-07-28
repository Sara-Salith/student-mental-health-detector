import streamlit as st

# -------------------------------------
# Page Configuration
# -------------------------------------

st.set_page_config(
    page_title="Assessment",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------------
# Login Check
# -------------------------------------

if "logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("app.py")

# -------------------------------------
# Title
# -------------------------------------

st.title("🎓 Student Mental Health Assessment")

st.write(f"### 👋 Welcome, **{st.session_state.user[1]}**")

st.info(
    "Please answer all questions honestly. "
    "Your responses will be analyzed using Machine Learning."
)

st.markdown("---")

# =====================================
# PERSONAL INFORMATION
# =====================================

st.subheader("👤 Personal Information")

col1, col2 = st.columns(2)

with col1:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

with col2:

    age = st.number_input(
        "Age",
        min_value=15,
        max_value=60,
        value=20
    )

cgpa = st.number_input(
    "CGPA",
    min_value=0.0,
    max_value=10.0,
    value=7.0
)

st.markdown("---")

# =====================================
# ACADEMIC
# =====================================

st.subheader("📚 Academic Information")

academic_pressure = st.slider(
    "Academic Pressure",
    0,
    5,
    3
)

study_satisfaction = st.slider(
    "Study Satisfaction",
    0,
    5,
    3
)

study_hours = st.number_input(
    "Study Hours Per Day",
    min_value=0.0,
    max_value=24.0,
    value=5.0
)

st.markdown("---")

# =====================================
# LIFESTYLE
# =====================================

st.subheader("🛌 Lifestyle")

sleep_duration = st.selectbox(
    "Sleep Duration",
    [
        "Less than 5 hours",
        "5-6 hours",
        "7-8 hours",
        "More than 8 hours"
    ]
)

dietary_habits = st.selectbox(
    "Dietary Habits",
    [
        "Unhealthy",
        "Moderate",
        "Healthy"
    ]
)

st.markdown("---")

# =====================================
# WELL BEING
# =====================================

st.subheader("💰 Personal Well-being")

financial_stress = st.slider(
    "Financial Stress",
    1,
    5,
    3
)

family_history = st.selectbox(
    "Family History of Mental Illness",
    [
        "No",
        "Yes"
    ]
)

suicidal_thoughts = st.selectbox(
    "Have you experienced suicidal thoughts?",
    [
        "No",
        "Yes"
    ]
)

st.markdown("---")

# =====================================
# BUTTON
# =====================================

if st.button(
    "🔍 Predict Mental Health Risk",
    use_container_width=True
):

    st.session_state.form_data = {

        "gender": gender,
        "age": age,
        "cgpa": cgpa,
        "academic_pressure": academic_pressure,
        "study_satisfaction": study_satisfaction,
        "study_hours": study_hours,
        "sleep_duration": sleep_duration,
        "dietary_habits": dietary_habits,
        "financial_stress": financial_stress,
        "family_history": family_history,
        "suicidal_thoughts": suicidal_thoughts

    }

    st.switch_page("pages/2_Result.py")