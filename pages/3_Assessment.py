import streamlit as st
import pandas as pd
import joblib
import os

from components.history import save_assessment
from components.navigation import result_page, login_page

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


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Assessment | Student Mental Health Detector",
    page_icon="🧠",
    layout="centered"
)


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
# LOAD MODEL
# ==================================================

@st.cache_resource
def load_model():

    model_paths = [
        "Model/mental_health_model.pkl",
        "mental_health_model.pkl",
        "Notebook/mental_health_model.pkl"
    ]

    for path in model_paths:

        if os.path.exists(path):
            return joblib.load(path)

    return None


# ==================================================
# HEADER
# ==================================================

st.markdown(
    """
    <h1 style="text-align:center;">
        🧠 Mental Health Assessment
    </h1>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <p style="text-align:center;color:#666;">
        Welcome, <b>{st.session_state.username}</b> 👋
    </p>
    """,
    unsafe_allow_html=True
)


st.write(
    "Please answer the following questions honestly. "
    "Your responses will be used to estimate your mental health risk."
)

st.divider()


# ==================================================
# INPUT FIELDS
# ==================================================

st.subheader("Student Information")


gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)


age = st.number_input(
    "Age",
    min_value=15,
    max_value=60,
    value=20
)


academic_pressure = st.slider(
    "Academic Pressure",
    min_value=0.0,
    max_value=5.0,
    value=3.0,
    step=0.5
)


work_pressure = st.slider(
    "Work Pressure",
    min_value=0.0,
    max_value=5.0,
    value=3.0,
    step=0.5
)


cgpa = st.number_input(
    "CGPA",
    min_value=0.0,
    max_value=10.0,
    value=7.0,
    step=0.1
)


study_satisfaction = st.slider(
    "Study Satisfaction",
    min_value=0.0,
    max_value=5.0,
    value=3.0,
    step=0.5
)


job_satisfaction = st.slider(
    "Job Satisfaction",
    min_value=0.0,
    max_value=5.0,
    value=3.0,
    step=0.5
)


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
        "Healthy",
        "Moderate",
        "Unhealthy"
    ]
)


suicidal_thoughts = st.selectbox(
    "Have you ever had suicidal thoughts?",
    ["Yes", "No"]
)


work_study_hours = st.slider(
    "Work/Study Hours",
    min_value=0,
    max_value=24,
    value=6
)


financial_stress = st.slider(
    "Financial Stress",
    min_value=0.0,
    max_value=5.0,
    value=3.0,
    step=0.5
)


family_history = st.selectbox(
    "Family History of Mental Illness",
    ["Yes", "No"]
)


# ==================================================
# PREDICT BUTTON
# ==================================================

st.divider()


if st.button(
    "🔍 Predict Mental Health Risk",
    use_container_width=True
):

    model = load_model()


    if model is None:

        st.error(
            "Model file not found. Please check "
            "mental_health_model.pkl."
        )

        st.stop()


    # ==================================================
    # ENCODING
    # ==================================================

    gender_encoded = (
        1 if gender == "Male" else 0
    )


    sleep_mapping = {
        "Less than 5 hours": 0,
        "5-6 hours": 1,
        "7-8 hours": 2,
        "More than 8 hours": 3
    }


    dietary_mapping = {
        "Healthy": 0,
        "Moderate": 1,
        "Unhealthy": 2
    }


    suicidal_encoded = (
        1 if suicidal_thoughts == "Yes" else 0
    )


    family_encoded = (
        1 if family_history == "Yes" else 0
    )


    sleep_encoded = sleep_mapping[
        sleep_duration
    ]


    dietary_encoded = dietary_mapping[
        dietary_habits
    ]


    # ==================================================
    # 13 FEATURES
    # ==================================================

    input_data = pd.DataFrame([[
        gender_encoded,
        age,
        academic_pressure,
        work_pressure,
        cgpa,
        study_satisfaction,
        job_satisfaction,
        sleep_encoded,
        dietary_encoded,
        suicidal_encoded,
        work_study_hours,
        financial_stress,
        family_encoded
    ]])


    # ==================================================
    # RUN MODEL
    # ==================================================

    try:

        # ----------------------------------------------
        # PREDICTION
        # ----------------------------------------------

        prediction = model.predict(
            input_data
        )[0]


        # ----------------------------------------------
        # RISK PROBABILITY
        # ----------------------------------------------

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(
                input_data
            )[0]

            classes = list(model.classes_)

            if 1 in classes:

                risk_index = classes.index(1)

                risk_score = (
                    probabilities[risk_index] * 100
                )

            else:

                risk_score = (
                    probabilities[-1] * 100
                )

        else:

            # Fallback if probability is unavailable
            risk_score = (
                100.0 if prediction == 1 else 0.0
            )


        # ----------------------------------------------
        # READABLE PREDICTION
        # ----------------------------------------------

        if prediction == 1 or str(prediction).lower() in [
            "yes",
            "depressed",
            "depression",
            "1"
        ]:

            prediction_text = (
                "Higher Mental Health Risk"
            )

        else:

            prediction_text = (
                "Lower Mental Health Risk"
            )


        # ==================================================
        # STUDENT DATA
        # ==================================================

        student_data = {

            "Gender": gender,

            "Age": age,

            "Academic Pressure":
                academic_pressure,

            "Work Pressure":
                work_pressure,

            "CGPA":
                cgpa,

            "Study Satisfaction":
                study_satisfaction,

            "Job Satisfaction":
                job_satisfaction,

            "Sleep Duration":
                sleep_duration,

            "Dietary Habits":
                dietary_habits,

            "Suicidal Thoughts":
                suicidal_thoughts,

            "Work/Study Hours":
                work_study_hours,

            "Financial Stress":
                financial_stress,

            "Family History":
                family_history
        }


        # ==================================================
        # SAVE ASSESSMENT HISTORY
        # ==================================================

        save_assessment(
            username=st.session_state.username,
            prediction=prediction_text,
            risk_score=risk_score,
            student_data=student_data
        )


        # ==================================================
        # STORE FOR RESULT PAGE
        # ==================================================

        st.session_state.assessment_data = (
            student_data
        )

        st.session_state.prediction = (
            prediction_text
        )

        st.session_state.risk_score = (
            risk_score
        )


        # ==================================================
        # GO TO RESULT
        # ==================================================

        st.switch_page(result_page)


    except Exception as e:

        st.error(
            "Prediction could not be completed."
        )

        st.code(str(e))