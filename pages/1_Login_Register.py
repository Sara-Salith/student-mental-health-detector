import streamlit as st
from components.auth import login_user, register_user


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Login | MindAura",
    page_icon="🧠",
    layout="centered"
)


# ==========================================
# SESSION STATE
# ==========================================

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #f8f7ff,
        #eef3ff,
        #fff5fb
    );
}


/* Main container */
.block-container {
    max-width: 850px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}


/* Hide unnecessary top spacing */
header {
    background: transparent !important;
}


/* Title */
.main-title {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 750;
    color: #293044;
    margin-bottom: 0.3rem;
}


/* Subtitle */
.subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 1.1rem;
    margin-bottom: 2.5rem;
}


/* Auth heading */
.auth-heading {
    text-align: center;
    font-size: 1.9rem;
    font-weight: 700;
    color: #293044;
    margin-bottom: 0.4rem;
}


/* Auth description */
.auth-description {
    text-align: center;
    color: #6b7280;
    margin-bottom: 1.8rem;
}


/* Bottom text */
.switch-text {
    text-align: center;
    color: #6b7280;
    margin-top: 1rem;
}


/* Input labels */
label {
    font-weight: 600 !important;
}


/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    min-height: 48px;
}


/* Main submit button */
div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    border: none;
    border-radius: 10px;
    background: linear-gradient(
        90deg,
        #ec4899,
        #7c3aed
    );
    color: white;
    font-weight: 650;
    min-height: 48px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# APP HEADER
# ==========================================

st.markdown(
    """
    <div class="main-title">
        🧠 Student Mental Health Detector
    </div>

    <div class="subtitle">
        AI-powered student mental health screening
    </div>
    """,
    unsafe_allow_html=True
)


# ======================================
# LOGIN PAGE
# ======================================

if st.session_state.auth_mode == "login":

    with st.container(border=True):

        st.markdown(
            """
            <div class="auth-heading">
                Welcome Back! 👋
            </div>

            <div class="auth-description">
                Login to continue your mental wellness journey.
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("login_form"):

            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            st.write("")

            submitted = st.form_submit_button(
                "Login"
            )


        if submitted:

            success = login_user(
                username,
                password
            )

            if success:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login successful! 🎉")

                from components.navigation import dashboard_page

                st.switch_page(
                    dashboard_page
                )

            else:

                st.error(
                    "Invalid username or password."
                )


        st.markdown(
            """
            <div class="switch-text">
                Don't have an account yet?
            </div>
            """,
            unsafe_allow_html=True
        )


        if st.button(
            "✨ Create a New Account",
            use_container_width=True,
            key="go_register"
        ):

            st.session_state.auth_mode = "register"
            st.rerun()


# ======================================
# REGISTER PAGE
# ======================================

else:

    with st.container(border=True):

        st.markdown(
            """
            <div class="auth-heading">
                Create Your Account ✨
            </div>

            <div class="auth-description">
                Start tracking and understanding your mental wellness.
            </div>
            """,
            unsafe_allow_html=True
        )


        with st.form("register_form"):

            username = st.text_input(
                "Choose Username",
                placeholder="Choose a username"
            )

            password = st.text_input(
                "Choose Password",
                type="password",
                placeholder="Create a password"
            )

            st.caption(
                "Password must contain at least 6 characters, "
                "including 1 uppercase letter, 1 lowercase letter, 1 number,"
                " and 1 special character."
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password"
            )

            st.write("")

            submitted = st.form_submit_button(
                "Create Account"
            )


        if submitted:

            success, message = register_user(
                username,
                password,
                confirm_password
            )

            if success:

                st.success(message)

                st.session_state.auth_mode = "login"

            else:

                st.error(message)


        st.markdown(
            """
            <div class="switch-text">
                Already have an account?
            </div>
            """,
            unsafe_allow_html=True
        )


        if st.button(
            "🔐 Login to Your Account",
            use_container_width=True,
            key="go_login"
        ):

            st.session_state.auth_mode = "login"
            st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.write("")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#9ca3af;
        font-size:0.85rem;
    ">
        🧠 MindAura AI • Student Mental Health Screening
        <br>
        AI-based educational assessment • Not a medical diagnosis
    </div>
    """,
    unsafe_allow_html=True
)