import streamlit as st

from utils import predict, ai_recommendation
from pdf_report import create_pdf

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Assessment Result",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# Check Login
# -----------------------------

if "logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("app.py")

if "form_data" not in st.session_state:
    st.warning("Please complete the assessment first.")
    st.switch_page("pages/1_Assessment.py")

# -----------------------------
# Get User Data
# -----------------------------

form_data = st.session_state.form_data

prediction, probability = predict(form_data)

risk_percentage = int(probability * 100)

# -----------------------------
# AI Recommendation
# -----------------------------

with st.spinner("🧠 AI Wellness Coach is assessing..."):

    recommendation = ai_recommendation(
        form_data,
        prediction
    )

if "user" in st.session_state:
    user_name = st.session_state.user[1].title()
else:
    user_name = "Student"

pdf_file = create_pdf(
    user_name=user_name,
    prediction=prediction,
    risk_percentage=risk_percentage,
    recommendation=recommendation
)

# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>

.main{
    background:#f5f7fb;
}

.title{
    font-size:38px;
    font-weight:bold;
    color:#1f2937;
}

.subtitle{
    font-size:18px;
    color:#6b7280;
}

.card{
    background:white;
    border-radius:15px;
    padding:25px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
    margin-top:20px;
}

.high-risk{
    background:#ffe5e5;
    border-left:8px solid #dc2626;
}

.low-risk{
    background:#e8fff1;
    border-left:8px solid #16a34a;
}

.section-title{
    font-size:24px;
    font-weight:bold;
    color:#1f2937;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Risk Card
# -----------------------------

st.markdown("<br>", unsafe_allow_html=True)

if prediction == 1:

    st.markdown(
        f"""
        <div class="card high-risk">

        <h2 style="color:#b91c1c;">
        🔴 High Mental Health Risk
        </h2>

        <h3>Risk Score</h3>

        <h1 style="font-size:50px;">
        {risk_percentage}%
        </h1>

        <p style="font-size:17px;">

        Your responses indicate a <b>higher level of mental health risk.</b>

        This assessment is intended for educational purposes and is <b>not a medical diagnosis.</b>

        Consider speaking with a trusted family member, friend, counselor, or mental health professional if you have ongoing concerns.

        </p>

        <hr>

        <p style="font-size:14px;color:gray;">

        ℹ️ <b>Disclaimer:</b> This assessment is intended for educational and screening purposes only.
        It is not a substitute for professional medical advice, diagnosis, or treatment.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
    

else:

    st.markdown(
        f"""
        <div class="card low-risk">

        <h2 style="color:#15803d;">
        🟢 Low Mental Health Risk
        </h2>

        <h3>Risk Score</h3>

        <h1 style="font-size:50px;">
        {risk_percentage}%
        </h1>

        <p style="font-size:17px;">

        Your responses indicate a <b>lower level of mental health risk.</b>

        Continue maintaining healthy habits, regular sleep, balanced nutrition, and good stress management practices.

        </p>

        <hr>

        <p style="font-size:14px;color:gray;">

        ℹ️ <b>Disclaimer:</b> This assessment is intended for educational and screening purposes only.
        It is not a substitute for professional medical advice, diagnosis, or treatment.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📊 Overall Risk Score")

    st.progress(risk_percentage / 100)

    st.caption(f"Estimated Risk Level: **{risk_percentage}%**")

    st.markdown("---")

    st.markdown(
        """
    <h2 style="color:#1f2937;">
    🤖 Personalized AI Wellness Coach
    </h2>
    """,
        unsafe_allow_html=True
    )

    # -----------------------------
# Header
# -----------------------------

styled_recommendation = f"""
<style>

h1 {{
    font-size: 30px !important;
    color: #1f2937;
    margin-top: 25px;
    margin-bottom: 12px;
}}

p {{
    font-size: 19px !important;
    line-height: 1.8;
    color: #374151;
}}

ul {{
    font-size: 19px !important;
    line-height: 1.8;
}}

li {{
    margin-bottom: 8px;
}}

</style>

<div class="card">

{recommendation}

</div>
"""

st.markdown(styled_recommendation, unsafe_allow_html=True)

st.markdown("---")

with open(pdf_file, "rb") as file:

    st.download_button(
        label="📄 Download Assessment Report",
        data=file,
        file_name=pdf_file,
        mime="application/pdf",
        use_container_width=True
    )

col1, col2 = st.columns(2)

with col1:

    if st.button("🔄 Take Assessment Again", use_container_width=True):

        st.switch_page("pages/1_Assessment.py")

with col2:

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.clear()

        st.switch_page("app.py")