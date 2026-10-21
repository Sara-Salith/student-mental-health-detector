import streamlit as st
import random
import time
import threading

st.set_page_config(
    page_title="Wellness Games | Mind Aura",
    page_icon="🎮",
    layout="wide"
)

# Back to Dashboard
if st.button("←", key="games_back", help="Back to Dashboard"):
    st.switch_page("pages/2_Dashboard.py")

# ---------------- SESSION STATE ----------------

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

if "memory_cards" not in st.session_state:
    st.session_state.memory_cards = []

if "memory_flipped" not in st.session_state:
    st.session_state.memory_flipped = []

if "memory_matched" not in st.session_state:
    st.session_state.memory_matched = []

if "memory_moves" not in st.session_state:
    st.session_state.memory_moves = 0

if "memory_started" not in st.session_state:
    st.session_state.memory_started = None

if "memory_finished" not in st.session_state:
    st.session_state.memory_finished = False


# ---------------- GAME FUNCTIONS ----------------

def start_memory_game():
    symbols = ["🌸", "🌈", "🌻", "🦋", "🍀", "🌙", "⭐", "💜"]

    cards = symbols * 2
    random.shuffle(cards)

    st.session_state.memory_cards = cards
    st.session_state.memory_flipped = []
    st.session_state.memory_matched = []
    st.session_state.memory_moves = 0
    st.session_state.memory_started = time.time()
    st.session_state.memory_finished = False


def flip_card(index):
    if st.session_state.memory_finished:
        return

    if index in st.session_state.memory_matched:
        return

    if index in st.session_state.memory_flipped:
        return

    if len(st.session_state.memory_flipped) >= 2:
        return

    st.session_state.memory_flipped.append(index)

    if len(st.session_state.memory_flipped) == 2:
        first, second = st.session_state.memory_flipped

        st.session_state.memory_moves += 1

        if (
            st.session_state.memory_cards[first]
            == st.session_state.memory_cards[second]
        ):
            st.session_state.memory_matched.extend(
                [first, second]
            )
            st.session_state.memory_flipped = []

            if len(st.session_state.memory_matched) == 16:
                st.session_state.memory_finished = True

        else:
            # Remember the mismatched cards temporarily.
            st.session_state.memory_mismatch = True


# ---------------- GAME SELECTION ----------------

st.markdown(
    """
    <style>
    .games-heading {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        color: #51418f;
    }

    .games-subtitle {
        text-align: center;
        color: #77738c;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .game-card {
        background: white;
        border: 1px solid #e4ddff;
        border-radius: 20px;
        padding: 25px 18px;
        text-align: center;
        min-height: 200px;
        box-shadow: 0 5px 20px rgba(85, 70, 140, 0.08);
    }

    .game-icon {
        font-size: 48px;
        margin-bottom: 12px;
    }

    .game-name {
        color: #51418f;
        font-size: 22px;
        font-weight: 750;
    }

    .game-description {
        color: #77738c;
        font-size: 14px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="games-heading">🎮 Mind Aura Wellness Games</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="games-subtitle">'
    'Take a break, relax your mind, and have fun! 🌷'
    '</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        """
        <div class="game-card">
            <div class="game-icon">🧠</div>
            <div class="game-name">Memory Match</div>
            <div class="game-description">
                Find matching pairs and train your memory.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🎮 Play Memory Match",
        key="open_memory_match",
        use_container_width=True
    ):
        st.switch_page("pages/8_Memory_Match.py")

with col2:
    st.markdown(
        """
        <div class="game-card">
            <div class="game-icon">🌬️</div>
            <div class="game-name">Breathing Challenge</div>
            <div class="game-description">
                Follow calming breathing exercises at your own pace.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🌬️ Start Breathing",
        key="open_breathing",
        use_container_width=True
    ):
        st.switch_page("pages/9_Breathing_Challenge.py")

with col3:
    st.markdown(
        """
        <div class="game-card">
            <div class="game-icon">🌷</div>
            <div class="game-name">Mood Garden</div>
            <div class="game-description">
                Plant flowers, nurture your garden, and earn points.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🌷 Enter Garden",
        key="open_mood_garden",
        use_container_width=True
    ):
        st.switch_page("pages/10_Mood_Garden.py")

st.stop()
# ---------------- PAGE DESIGN ----------------

st.markdown(
    """
    <style>
    .stApp {
        background: #fbfaff;
    }

    .game-heading {
        color: #51418f;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .game-subtitle {
        color: #74718b;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .game-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #e7e0ff;
        box-shadow: 0 5px 20px rgba(100, 75, 180, 0.08);
        text-align: center;
    }

    div.stButton > button {
        border-radius: 12px;
        border: 1px solid #ded5ff;
        min-height: 65px;
        font-size: 27px;
        background: white;
        color: #51418f;
        transition: 0.2s;
    }

    div.stButton > button:hover {
        background: #f0ebff;
        border-color: #a78bfa;
        color: #51418f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-heading">🧠 Memory Match</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">'
    'Find all eight matching pairs and give your mind a playful break!'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "How to play: Select two cards at a time. "
    "Find matching symbols using as few moves as possible."
)

# ---------------- START GAME ----------------

if not st.session_state.memory_cards:
    st.markdown(
        """
        <div class="game-card">
            <h2>🌸 Ready to play?</h2>
            <p>Find all 8 matching pairs hidden in 16 cards.</p>
            <p>Take your time and enjoy the game!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🎮 Start Memory Match",
        use_container_width=True
    ):
        start_memory_game()
        st.rerun()

else:

    # ---------------- STATISTICS ----------------

    matched_pairs = len(st.session_state.memory_matched) // 2

    if st.session_state.memory_finished:
        elapsed = int(
            time.time() - st.session_state.memory_started
        )
    else:
        elapsed = int(
            time.time() - st.session_state.memory_started
        )

    minutes = elapsed // 60
    seconds = elapsed % 60

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("⭐ Matched Pairs", f"{matched_pairs}/8")

    with col2:
        st.metric("🔄 Moves", st.session_state.memory_moves)

    with col3:
        st.metric("⏱️ Time", f"{minutes:02d}:{seconds:02d}")

    st.write("")

    # ---------------- MEMORY BOARD ----------------

    for row in range(4):
        cols = st.columns(4, gap="medium")

        for col in range(4):
            index = row * 4 + col

            with cols[col]:

                if (
                    index in st.session_state.memory_matched
                    or index in st.session_state.memory_flipped
                ):
                    label = st.session_state.memory_cards[index]
                else:
                    label = "❔"

                disabled = (
                    index in st.session_state.memory_matched
                    or st.session_state.memory_finished
                )

                if st.button(
                    label,
                    key=f"memory_card_{index}",
                    use_container_width=True,
                    disabled=disabled
                ):
                    flip_card(index)
                    st.rerun()

    # ---------------- HANDLE MISMATCH ----------------

    if st.session_state.get("memory_mismatch", False):
        time.sleep(1)

        st.session_state.memory_flipped = []
        st.session_state.memory_mismatch = False

        st.rerun()

    # ---------------- GAME COMPLETE ----------------

    if st.session_state.memory_finished:
        st.balloons()

        st.success(
            "🎉 Congratulations! You found every matching pair!"
        )

        st.markdown(
            f"""
            <div class="game-card">
                <h2>🌟 Well played!</h2>
                <p>You completed the game in
                <b>{st.session_state.memory_moves} moves</b>.</p>
                <p>Total time: <b>{minutes:02d}:{seconds:02d}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------- RESTART ----------------

    st.write("")

    if st.button(
        "🔄 Restart Game",
        use_container_width=True
    ):
        start_memory_game()
        st.rerun()