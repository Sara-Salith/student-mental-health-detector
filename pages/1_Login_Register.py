import streamlit as st

from components.auth import login_user, register_user
from components.navigation import dashboard_page


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
    page_title="Login | Student Mental Health Detector",
    page_icon="🧠",
    layout="centered"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.markdown(
    """
    <h1 style="text-align:center;">
        🧠 Student Mental Health Detector
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="text-align:center;color:#666;">
        AI-powered student mental health screening
    </p>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# LOGIN / REGISTER TABS
# --------------------------------------------------

login_tab, register_tab = st.tabs(
    ["🔐 Login", "📝 Register"]
)


# ==================================================
# LOGIN
# ==================================================

with login_tab:

    st.subheader("Welcome Back!")

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        if login_user(username, password):

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("Login successful!")

            st.switch_page(dashboard_page)

        else:

            st.error("Invalid username or password.")


# ==================================================
# REGISTER
# ==================================================

with register_tab:

    st.subheader("Create Account")

    new_username = st.text_input(
        "Choose Username",
        key="register_username"
    )

    new_password = st.text_input(
        "Choose Password",
        type="password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )

    if st.button(
        "Register",
        use_container_width=True
    ):

        success, message = register_user(
            new_username,
            new_password,
            confirm_password
        )

        if success:
            st.success(message)
        else:
            st.error(message)