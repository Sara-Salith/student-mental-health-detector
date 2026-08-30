import streamlit as st
import pandas as pd
import joblib
import os

from components.history import save_assessment
from components.navigation import (
    login_page,
    assessment_page,
    dashboard_page,
    result_page,
    back_button
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Mental Health Assessment | MindAura AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
========================================================= */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(37, 99, 235, 0.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 90%,
            rgba(20, 184, 166, 0.10),
            transparent 30%
        ),
        #F8FAFC;
}

.block-container {
    max-width: 1180px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}


/* =========================================================
   BRAND
========================================================= */

.brand-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 28px;
}

.brand-icon {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    background: linear-gradient(
        135deg,
        #2563EB,
        #7C3AED
    );
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    box-shadow:
        0 8px 22px rgba(37, 99, 235, 0.25);
}

.brand-name {
    font-size: 24px;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.1;
}

.brand-caption {
    font-size: 12px;
    color: #64748B;
    margin-top: 4px;
}


/* =========================================================
   HERO
========================================================= */

.hero-card {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(
            135deg,
            #0F172A,
            #172554
        );
    border-radius: 24px;
    padding: 42px 45px;
    margin-bottom: 25px;
    box-shadow:
        0 18px 45px rgba(15, 23, 42, 0.16);
}

.hero-card::after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    background: rgba(96, 165, 250, 0.20);
    right: -70px;
    top: -80px;
}

.hero-title {
    position: relative;
    z-index: 2;
    font-size: 38px;
    font-weight: 800;
    color: white;
    line-height: 1.2;
    margin-bottom: 16px;
}

.hero-title span {
    background:
        linear-gradient(
            90deg,
            #60A5FA,
            #A78BFA,
            #2DD4BF
        );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    position: relative;
    z-index: 2;
    max-width: 760px;
    color: #CBD5E1;
    font-size: 15px;
    line-height: 1.7;
}

.hero-description b {
    color: white;
}

.hero-meta {
    position: relative;
    z-index: 2;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 25px;
}

.meta-pill {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.12);
    color: #E2E8F0;
    padding: 8px 13px;
    border-radius: 30px;
    font-size: 12px;
}


/* =========================================================
   PROGRESS
========================================================= */

.progress-card {
    background: white;
    border-radius: 18px;
    padding: 18px 22px;
    border: 1px solid #E2E8F0;
    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);
    margin-bottom: 25px;
}

.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    color: #64748B;
    margin-bottom: 10px;
}

.progress-track {
    width: 100%;
    height: 7px;
    background: #E2E8F0;
    border-radius: 20px;
    overflow: hidden;
}

.progress-fill {
    width: 100%;
    height: 100%;
    border-radius: 20px;
    background:
        linear-gradient(
            90deg,
            #2563EB,
            #7C3AED,
            #14B8A6
        );
}


/* =========================================================
   SECTION CARDS
========================================================= */

.section-card {
    background: rgba(255,255,255,0.94);
    border: 1px solid #E2E8F0;
    border-radius: 22px;
    padding: 28px 30px 22px 30px;
    margin-bottom: 22px;
    box-shadow:
        0 10px 30px rgba(15,23,42,0.05);
}

.section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 8px;
}

.section-icon {
    width: 44px;
    height: 44px;
    border-radius: 13px;
    background: #EFF6FF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #0F172A;
}

.section-description {
    color: #64748B;
    font-size: 13px;
    margin-bottom: 20px;
}


/* =========================================================
   LABELS
========================================================= */

.stSelectbox label,
.stNumberInput label,
.stSlider label {
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}


/* =========================================================
   INPUTS
========================================================= */

.stSelectbox > div > div,
.stNumberInput input {
    background: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 12px !important;
}

.stSelectbox > div > div:hover,
.stNumberInput input:hover {
    border-color: #60A5FA !important;
}


/* =========================================================
   SLIDERS
========================================================= */

.stSlider {
    padding-top: 5px;
    padding-bottom: 8px;
}

.stSlider [data-baseweb="slider"] {
    margin-top: 4px;
}


/* =========================================================
   PRIVACY / INFO BOX
========================================================= */

.privacy-card {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 16px;
    padding: 17px 20px;
    color: #1E40AF;
    font-size: 13px;
    line-height: 1.6;
    margin: 10px 0 25px;
}


/* =========================================================
   PREDICT BUTTON
========================================================= */

div.stButton > button {
    height: 58px;
    border-radius: 15px;
    border: none;
    background:
        linear-gradient(
            90deg,
            #2563EB,
            #7C3AED
        );
    color: white;
    font-size: 16px;
    font-weight: 700;
    box-shadow:
        0 10px 25px rgba(37,99,235,0.25);
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 14px 32px rgba(37,99,235,0.35);
}


/* =========================================================
   FOOTER
========================================================= */

.assessment-footer {
    text-align: center;
    color: #94A3B8;
    font-size: 12px;
    margin-top: 30px;
    line-height: 1.7;
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .hero-card {
        padding: 30px 25px;
    }

    .hero-title {
        font-size: 30px;
    }

    .section-card {
        padding: 22px 20px;
    }

    .brand-name {
        font-size: 21px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOGIN CHECK
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.warning("Please login first.")

    if st.button("Go to Login"):
        st.switch_page(login_page)

    st.stop()

back_button(dashboard_page, "back_to_dashboard")


# ============================================================
# LOAD MODEL
# ============================================================

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


# ============================================================
# BRAND
# ============================================================

st.html("""
<div class="brand-row">
    <div class="brand-icon">🧠</div>

    <div>
        <div class="brand-name">MindAura AI</div>
        <div class="brand-caption">
            Student Mental Health Risk Detector
        </div>
    </div>
</div>
""")

# ============================================================
# HERO
# ============================================================

username = st.session_state.get("username", "Student")

st.html(f"""
<div class="hero-card">

    <div class="hero-title">
        Your Mental <span>Wellness</span> Assessment
    </div>

    <div class="hero-description">
        Welcome back, <b>{username}</b> 👋
        <br><br>

        Answer a few questions about your academic,
        lifestyle and emotional wellbeing. Our AI model
        will analyze these factors and provide an
        estimated mental health risk assessment.
    </div>

    <div class="hero-meta">

        <div class="meta-pill">🧠 AI-Powered</div>
        <div class="meta-pill">⏱️ 2–3 minutes</div>
        <div class="meta-pill">🔒 Private & Secure</div>
        <div class="meta-pill">📊 Personalized Analysis</div>

    </div>

</div>
""")

# ============================================================
# PROGRESS
# ============================================================

st.html("""
<div class="progress-card">

    <div class="progress-label">
        <span>Assessment Progress</span>
        <span>Step 4 of 4</span>
    </div>

    <div class="progress-track">
        <div class="progress-fill"></div>
    </div>

</div>
""")


st.html("""
<div class="privacy-card">

    🔒 <b>Your responses are treated as private assessment data.</b>

    <br>

    This tool provides an AI-based educational risk estimate
    and does not replace professional mental health diagnosis
    or care.

</div>
""")


# ============================================================
# SECTION 1 — PERSONAL PROFILE
# ============================================================

st.html("""
<div class="section-card">

    <div class="section-header">

        <div class="section-icon">
            👤
        </div>

        <div class="section-title">
            Personal Profile
        </div>

    </div>

    <div class="section-description">
        Tell us a little about yourself so the assessment
        can understand your personal context.
    </div>

</div>
""")


col1, col2 = st.columns(2)


with col1:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        help="Select your gender identity."
    )


with col2:

    age = st.number_input(
        "Age",
        min_value=15,
        max_value=60,
        value=20
    )


# ============================================================
# SECTION 2 — ACADEMIC WELLBEING
# ============================================================

st.html("""
<div class="section-card">

    <div class="section-header">

        <div class="section-icon">
            🎓
        </div>

        <div class="section-title">
            Academic Wellbeing
        </div>

    </div>

    <div class="section-description">
        Academic pressure and satisfaction can strongly
        influence overall student wellbeing.
    </div>

</div>
""")


col1, col2 = st.columns(2)


with col1:

    academic_pressure = st.slider(
        "Academic Pressure",
        min_value=0.0,
        max_value=5.0,
        value=3.0,
        step=0.5,
        help="Rate the academic pressure you currently experience."
    )


with col2:

    study_satisfaction = st.slider(
        "Study Satisfaction",
        min_value=0.0,
        max_value=5.0,
        value=3.0,
        step=0.5,
        help="How satisfied are you with your current studies?"
    )


col1, col2 = st.columns(2)


with col1:

    work_pressure = st.slider(
        "Work Pressure",
        min_value=0.0,
        max_value=5.0,
        value=3.0,
        step=0.5,
        help="Rate the pressure you experience from work or responsibilities."
    )


with col2:

    job_satisfaction = st.slider(
        "Job Satisfaction",
        min_value=0.0,
        max_value=5.0,
        value=3.0,
        step=0.5,
        help="How satisfied are you with your work or career situation?"
    )


col1, col2 = st.columns(2)


with col1:

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=10.0,
        value=7.0,
        step=0.1,
        help="Enter your current CGPA."
    )


with col2:

    work_study_hours = st.slider(
        "Work / Study Hours per Day",
        min_value=0,
        max_value=24,
        value=6,
        help="Approximate number of hours spent working or studying each day."
    )


# ============================================================
# SECTION 3 — LIFESTYLE
# ============================================================

st.html("""
<div class="section-card">

    <div class="section-header">

        <div class="section-icon">
            🌙
        </div>

        <div class="section-title">
            Lifestyle & Wellness
        </div>

    </div>

    <div class="section-description">
        Sleep, nutrition and daily habits can play an
        important role in mental wellbeing.
    </div>

</div>
""")


col1, col2 = st.columns(2)


with col1:

    sleep_duration = st.selectbox(
        "Sleep Duration",
        [
            "Less than 5 hours",
            "5-6 hours",
            "7-8 hours",
            "More than 8 hours"
        ],
        help="Choose the amount of sleep you usually get."
    )


with col2:

    dietary_habits = st.selectbox(
        "Dietary Habits",
        [
            "Healthy",
            "Moderate",
            "Unhealthy"
        ],
        help="Select the option that best describes your usual diet."
    )


financial_stress = st.slider(
    "Financial Stress",
    min_value=0.0,
    max_value=5.0,
    value=3.0,
    step=0.5,
    help="Rate the financial stress you currently experience."
)


# ============================================================
# SECTION 4 — MENTAL WELLBEING
# ============================================================

st.html("""
<div class="section-card">

    <div class="section-header">

        <div class="section-icon">
            ❤️
        </div>

        <div class="section-title">
            Mental Wellbeing
        </div>

    </div>

    <div class="section-description">
        These questions help the model understand emotional
        and psychological factors associated with wellbeing.
    </div>

</div>
""")


col1, col2 = st.columns(2)


with col1:

    suicidal_thoughts = st.selectbox(
        "Have you ever had suicidal thoughts?",
        ["Yes", "No"],
        help="Please answer honestly. Your response is used only as an assessment feature."
    )


with col2:

    family_history = st.selectbox(
        "Family History of Mental Illness",
        ["Yes", "No"],
        help="Select whether there is a known family history."
    )


# ============================================================
# READY CARD
# ============================================================

st.html("""
<div class="privacy-card">

    💡 <b>Almost there!</b>

    <br><br>

    You've completed the assessment questions.
    Click the button below to let the AI model analyze
    your responses and estimate your current risk level.

</div>
""")


# ============================================================
# PREDICTION
# ============================================================

if st.button(
    "🧠  Analyze My Mental Health Risk",
    use_container_width=True
):

    model = load_model()


    if model is None:

        st.error(
            "Model file not found. Please check "
            "mental_health_model.pkl."
        )

        st.stop()


    # ========================================================
    # ENCODING
    # ========================================================

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


    # ========================================================
    # 13 FEATURES
    # ========================================================

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


    # ========================================================
    # RUN MODEL
    # ========================================================

    try:

        with st.spinner(
            "🧠 AI is analyzing your responses..."
        ):

            prediction = model.predict(
                input_data
            )[0]


            # ==================================================
            # RISK PROBABILITY
            # ==================================================

            if hasattr(model, "predict_proba"):

                probabilities = model.predict_proba(
                    input_data
                )[0]


                classes = list(
                    model.classes_
                )


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

                risk_score = (
                    100.0
                    if prediction == 1
                    else 0.0
                )


            # ==================================================
            # READABLE PREDICTION
            # ==================================================

            if (
                prediction == 1
                or str(prediction).lower()
                in [
                    "yes",
                    "depressed",
                    "depression",
                    "1"
                ]
            ):

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
            # SAVE HISTORY
            # ==================================================

            save_assessment(
                username=st.session_state.username,
                prediction=prediction_text,
                risk_score=risk_score,
                student_data=student_data
            )


            # ==================================================
            # STORE RESULT
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


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="assessment-footer">

    MindAura AI • Student Mental Health Risk Detector

    <br>

    AI-based educational assessment • Not a medical diagnosis

</div>
""")