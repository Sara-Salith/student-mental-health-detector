import streamlit as st

from components.history import get_user_history

from components.navigation import (
    dashboard_page,
    back_button
)



# ==================================================
# CHECK LOGIN
# ==================================================

if not st.session_state.get("logged_in", False):

    st.warning("Please login first.")
    st.stop()


username = st.session_state.username

back_button(dashboard_page, "back_to_dashboard_history")


# ==================================================
# PAGE
# ==================================================

st.title("📋 Assessment History")

st.write(
    f"Here are your previous assessments, {username}."
)


history = get_user_history(username)


if history.empty:

    st.info(
        "You haven't completed any assessments yet."
    )

else:

    st.dataframe(
        history[
            [
                "timestamp",
                "prediction",
                "risk_score"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )