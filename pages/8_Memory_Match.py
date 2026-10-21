import streamlit as st
import random
import time

st.set_page_config(
    page_title="Memory Match | Mind Aura",
    page_icon="🧠",
    layout="wide"
)

# Back button
if st.button("⬅️ Back to Games"):
    st.switch_page("pages/7_Wellness_Games.py")

# Check login
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access this game.")
    st.stop()

# ---------------- SESSION STATE ----------------

if "memory_cards" not in st.session_state:
    st.session_state.memory_cards = []

if "memory_flipped" not in st.session_state:
    st.session_state.memory_flipped = []

if "memory_matched" not in st.session_state:
    st.session_state.memory_matched = []

if "memory_moves" not in st.session_state:
    st.session_state.memory_moves = 0

if "memory_started" not in st.session_state:
    st.session_state.memory_started = 0

if "memory_finished" not in st.session_state:
    st.session_state.memory_finished = False

if "memory_mismatch" not in st.session_state:
    st.session_state.memory_mismatch = False

st.title("🧠 Memory Match")
st.write("Your Memory Match game will appear here.")

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

# ---------------- HOW TO PLAY ----------------

with st.expander("🎮 How to Play Memory Match", expanded=True):

    st.markdown("""
    ### 🎯 Your Goal
    Find all 8 matching pairs hidden among 16 cards.

    ### 🕹️ How to Play
    1. Click **Start Memory Match**.
    2. Click any card to reveal its symbol.
    3. Click another card to reveal the second symbol.
    4. **Matching cards:** They stay open.
    5. **Non-matching cards:** They turn face down again.
    6. Remember the symbols and where you saw them!

    ### 🏆 How to Win
    Match all 8 pairs to complete the game.

    ### 💡 Example
    You reveal 🌻 and then 🌷. They don't match,
    so remember their positions and try again!

    **Tip:** The fewer moves you use, the better!
    """)

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