import streamlit as st


# ==================================================
# PAGE DEFINITIONS
# ==================================================

login_page = st.Page(
    "pages/1_Login_Register.py",
    title="Login / Register",
    url_path="login",
    icon="🔐"
)

dashboard_page = st.Page(
    "pages/2_Dashboard.py",
    title="Dashboard",
    url_path="dashboard",
    icon="🏠"
)

assessment_page = st.Page(
    "pages/3_Assessment.py",
    title="Assessment",
    url_path="assessment",
    icon="🧠"
)

result_page = st.Page(
    "pages/4_Result.py",
    title="Result",
    url_path="result",
    icon="📊"
)

history_page = st.Page(
    "pages/5_History.py",
    title="History",
    url_path="history",
    icon="📋"
)

download_report_page = st.Page(
    "pages/6_Download_Report.py",
    title="Download Report",
    url_path="download-report",
    icon="📄"
)


# ==================================================
# BACK BUTTON
# ==================================================

def back_button(page, key):

    if st.button(
        "← Back",
        key=key,
        use_container_width=False
    ):
        st.switch_page(page)