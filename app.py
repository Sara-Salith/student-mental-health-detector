import streamlit as st
from auth import register, login

import re

def strong_password(password):
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"[0-9]", password)
    )

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="AI Student Mental Health Detector",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- Hide Streamlit UI ----------------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stSidebar"]{
    display:none;
}

.block-container{
    padding-top:2rem;
}

.title{
    text-align:center;
    font-size:46px;
    font-weight:bold;
    color:#2E4053;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
    margin-bottom:30px;
}

.login-box{
    background:white;
    padding:35px;
    border-radius:18px;
    box-shadow:0px 5px 20px rgba(0,0,0,0.12);
}
</style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------

st.markdown("""
<div class="subtitle">
Predict • Analyze • Improve
</div>

<div style="
text-align:center;
font-size:18px;
color:#555;
margin-bottom:30px;
">
A secure AI-powered platform that analyzes academic,
lifestyle and psychological factors to provide
personalized mental wellness recommendations.
</div>
""", unsafe_allow_html=True)

# ---------------- Login/Register Tabs ----------------

login_tab, register_tab = st.tabs(["🔑 Login", "📝 Register"])

# ======================================================
# LOGIN
# ======================================================

with login_tab:

    st.subheader("Welcome Back!")

    email = st.text_input(
        "📧Email",
        key="login_email"
    )

    password = st.text_input(
        "🔒Password",
        type="password",
        key="login_password"
    )

    if st.button("Login", use_container_width=True):

        with st.spinner("Logging in..."):

         user = login(email, password)

        if user:

            st.session_state.logged_in = True
            st.session_state.user = user

            st.success(f"Welcome {user[1]} 🎉")

            st.switch_page("pages/1_Assessment.py")

        else:

            st.error("Invalid Email or Password")


# ======================================================
# REGISTER
# ======================================================

with register_tab:

    st.subheader("Create Account")

    name = st.text_input(
        "👤 Full Name",
        key="register_name"
    )

    email = st.text_input(
        "📧Email",
        key="register_email"
    )

    password = st.text_input(
        "🔒Password",
        type="password",
        key="register_password"
    )

    confirm = st.text_input(
        "🔒Confirm Password",
        type="password"
    )

    if st.button("Create Account", use_container_width=True):

        if password != confirm:

            st.error("Passwords do not match.")

        elif not strong_password(password):

         st.warning("""
 Password must contain:

 ✔ At least 8 characters

 ✔ One uppercase letter

 ✔ One lowercase letter

 ✔ One number
 """)
        else:

            with st.spinner("Creating your account..."):

                success = register(name, email, password)

            if success:

                st.success("Account Created Successfully!")

                st.info("Please Login using your credentials.")

            else:

                st.error("Email already exists.")