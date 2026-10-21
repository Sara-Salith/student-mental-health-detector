import streamlit as st

st.set_page_config(
    page_title="Mood Garden | Mind Aura",
    page_icon="🌷",
    layout="wide"
)

# Back button
if st.button("⬅️ Back to Games"):
    st.switch_page("pages/7_Wellness_Games.py")

# Check login
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access this game.")
    st.stop()

# Load the existing game
from games.mood_garden import render_mood_garden

render_mood_garden()