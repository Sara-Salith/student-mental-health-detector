import streamlit as st
import streamlit.components.v1 as components
import json
import random
from datetime import date
from components.auth import get_supabase, get_supabase_admin

# --------------------------------------------------
# MOOD GARDEN - MIND AURA
# --------------------------------------------------

def render_mood_garden():

    # ---------------- INITIAL STATE ----------------

    defaults = {
        "mg_plants": [],
        "mg_points": 0,
        "mg_level": 1,
        "mg_mood_history": [],
        "mg_last_checkin": "",
        "mg_selected_seed": "🌻 Sunflower",
        "mg_decorations": ["🪨"],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Load saved garden progress from Supabase
    if not st.session_state.get("mg_garden_loaded", False):
        try:
            username = st.session_state.get("username")

            if username:
                supabase = get_supabase_admin()

                response = (
                    supabase.table("mood_garden_progress")
                    .select("*")
                    .eq("username", username)
                    .execute()
                )

                saved = response.data[0] if response.data else None

                if saved:
                    st.session_state.mg_plants = saved["plants"]
                    st.session_state.mg_points = saved["points"]
                    st.session_state.mg_level = saved["level"]
                    st.session_state.mg_decorations = saved["decorations"]
                    st.session_state.mg_selected_seed = saved["selected_seed"]

                    if st.session_state.mg_selected_seed == "sunflower": 
                        st.session_state.mg_selected_seed = "🌻 Sunflower"

            st.session_state.mg_garden_loaded = True

        except Exception as e:
            st.error(f"Could not load garden progress: {e}")

    # Load saved mood history from Supabase
    if not st.session_state.get("mg_history_loaded", False):
        try:
            supabase = get_supabase_admin()
            username = st.session_state.get("username")

            if username:
                response = (
                    supabase.table("mood_history")
                    .select("mood, mood_date")
                    .eq("username", username)
                    .order("mood_date", desc=True)
                    .execute()
                )

                st.session_state.mg_mood_history = [
                    {
                        "date": str(row["mood_date"]),
                        "mood": row["mood"]
                    }
                    for row in response.data
                ]

            st.session_state.mg_history_loaded = True

        except Exception as e:
            st.error(f"Could not load mood history: {e}")

    seeds = {
        "🌻 Sunflower": {
            "emoji": "🌻",
            "cost": 0,
            "description": "A cheerful flower full of sunshine."
        },
        "🌷 Tulip": {
            "emoji": "🌷",
            "cost": 10,
            "description": "A beautiful symbol of new beginnings."
        },
        "🌹 Rose": {
            "emoji": "🌹",
            "cost": 20,
            "description": "A reminder to treat yourself with kindness."
        },
        "🌸 Cherry Blossom": {
            "emoji": "🌸",
            "cost": 30,
            "description": "A gentle reminder that growth takes time."
        },
        "🌼 Daisy": {
            "emoji": "🌼",
            "cost": 15,
            "description": "A little flower for brighter days."
        },
    }

    moods = {
        "😊 Happy": "Keep nurturing the things that bring you joy!",
        "😌 Calm": "Enjoy this peaceful moment. You deserve it.",
        "😟 Anxious": "Take things one step at a time. You don't have to solve everything now.",
        "😢 Sad": "It's okay to have difficult days. Treat yourself gently.",
        "😣 Stressed": "Pause for a moment. One small step is enough.",
        "😴 Tired": "Rest is productive too. Give yourself permission to recharge.",
    }

    # ---------------- HELPERS ----------------

    def add_points(amount):
        st.session_state.mg_points += amount
        st.session_state.mg_level = (
            st.session_state.mg_points // 50
        ) + 1

        save_garden_progress()

    def save_garden_progress():
        username = st.session_state.get("username")

        if not username:
            st.error("Please log in to save your garden.")
            return

        try:
            supabase = get_supabase_admin()

            supabase.table("mood_garden_progress").upsert({
                "username": username,
                "plants": st.session_state.mg_plants,
                "points": st.session_state.mg_points,
                "level": st.session_state.mg_level,
                "decorations": st.session_state.mg_decorations,
                "selected_seed": st.session_state.mg_selected_seed,
            }, on_conflict="username").execute()

        except Exception as e:
            st.error(f"Could not save garden progress: {e}")

    def plant_seed():
        selected = st.session_state.mg_selected_seed
        seed = seeds[selected]

        if st.session_state.mg_points < seed["cost"]:
            st.warning(
                f"You need {seed['cost']} garden points "
                "to unlock this seed."
            )
            return

        if seed["cost"] > 0:
            st.session_state.mg_points -= seed["cost"]

        plant = {
            "name": selected,
            "emoji": seed["emoji"],
            "watered": False,
            "growth": 0,
            "id": random.randint(100000, 999999),
        }

        st.session_state.mg_plants.append(plant)
        st.session_state.mg_level = (
            st.session_state.mg_points // 50
        ) + 1

        st.session_state["mg_notice"] = (
            f"{seed['emoji']} Your {selected} seed has been planted!"
        )

        save_garden_progress()

    def water_plant(index):
        plant = st.session_state.mg_plants[index]

        if plant["watered"]:
            st.warning("This plant has already been watered!")
            return

        plant["watered"] = True
        plant["growth"] = min(plant["growth"] + 1, 3)

        add_points(5)

        st.session_state["mg_notice"] = (
            f"💧 You watered your {plant['name']}! +5 points"
        )

        save_garden_progress()


    # ---------------- STYLING ----------------

    st.markdown(
        """
        <style>
        .stApp {
            background:
                linear-gradient(180deg, #f8f7ff 0%, #f0fff4 100%);
        }

        .mg-title {
            text-align: center;
            color: #51418f;
            font-size: 38px;
            font-weight: 850;
            margin-bottom: 3px;
        }

        .mg-subtitle {
            text-align: center;
            color: #77738c;
            font-size: 16px;
            margin-bottom: 25px;
        }

        .mg-panel {
            background: rgba(255,255,255,0.92);
            border: 1px solid #e4ddff;
            border-radius: 20px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 5px 20px rgba(85,70,140,0.07);
        }

        .mg-stat {
            text-align: center;
            padding: 14px 6px;
            background: white;
            border: 1px solid #e4ddff;
            border-radius: 16px;
        }

        .mg-stat-number {
            color: #51418f;
            font-size: 27px;
            font-weight: 800;
        }

        .mg-stat-label {
            color: #77738c;
            font-size: 13px;
        }

        .mg-ground {
            background: linear-gradient(
                180deg,
                #dff4ff 0%,
                #e8f8e7 46%,
                #b8df9d 47%,
                #8dc47b 100%
            );
            border-radius: 22px;
            padding: 22px 12px;
            border: 2px solid #c7e7bd;
            min-height: 175px;
            text-align: center;
            overflow: hidden;
        }

        .mg-ground-title {
            color: #41634a;
            font-size: 14px;
            font-weight: 700;
        }

        .mg-empty {
            color: #52796f;
            font-size: 16px;
            padding: 20px 5px;
        }

        .mg-plant {
            display: inline-block;
            font-size: 42px;
            padding: 10px 12px;
            animation: mg-sway 3s ease-in-out infinite;
        }

        @keyframes mg-sway {
            0%, 100% { transform: rotate(-3deg); }
            50% { transform: rotate(3deg); }
        }

        .mg-decoration {
            display: inline-block;
            font-size: 28px;
            margin: 5px;
        }

        .mg-note {
            background: #f3efff;
            color: #51418f;
            border-radius: 14px;
            padding: 15px;
            margin: 10px 0;
        }

        div.stButton > button {
            border-radius: 12px;
            min-height: 43px;
            border: 1px solid #dcd2ff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------------- HOW TO PLAY ----------------

    with st.expander("🌷 How to Play Mood Garden", expanded=True):

        st.markdown("""
        ### 💗 1. Record Your Mood
        Choose how you're feeling today and click
        **Record My Mood** to save your check-in.

        ### ⭐ 2. Earn Garden Points
        - Record your mood to earn 10 points.
        - Water a plant to earn 5 points.
        - Use your points to unlock new seeds and decorations.

        ### 🌱 3. Plant Flowers
        Choose a seed from the planting section.
        Sunflowers are free, while other flowers cost points.
    
        ### 💧 4. Grow Your Garden
        Water your plants to help them grow through
        different stages until they mature.

        ### 🦋 5. Customize Your Garden
        Unlock decorations such as butterflies, trees,
        birds, and lilies using your garden points.
    
        ### 🏆 6. Level Up
        Earn points to increase your garden level.
        Check your progress using the bar near the top.
    
        ### 📅 7. Review Your Mood History
        Open **My Mood History** to see your saved
        mood check-ins.
    
        """)
    
        st.info(
            "💜 Your garden is a place for self-care, not competition. "
            "There are no bad moods, and you can grow at your own pace."
        )

    # ---------------- HEADER ----------------

    st.markdown(
        '<div class="mg-title">🌷 My Mood Garden</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="mg-subtitle">'
        'Plant kindness. Grow at your own pace. 🌿'
        '</div>',
        unsafe_allow_html=True
    )

    # ---------------- STATS ----------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="mg-stat">
                <div class="mg-stat-number">
                    ⭐ {st.session_state.mg_points}
                </div>
                <div class="mg-stat-label">Garden Points</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="mg-stat">
                <div class="mg-stat-number">
                    🌱 {len(st.session_state.mg_plants)}
                </div>
                <div class="mg-stat-label">Plants</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="mg-stat">
                <div class="mg-stat-number">
                    🏆 {st.session_state.mg_level}
                </div>
                <div class="mg-stat-label">Garden Level</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.progress(
        (st.session_state.mg_points % 50) / 50,
        text="Progress towards your next level"
    )

    # ---------------- NOTICES ----------------

    if st.session_state.get("mg_notice"):
        st.success(st.session_state.mg_notice)
        del st.session_state["mg_notice"]

    # ---------------- MOOD CHECK-IN ----------------

    st.markdown("## 💗 Today's Mood Check-in")

    mood = st.selectbox(
        "How are you feeling right now?",
        list(moods.keys()),
        key="mg_mood_selector"
    )

    if st.button(
        "💗 Record My Mood",
        use_container_width=True,
        key="mg_record_mood"
    ):
        today = date.today().isoformat()
        username = st.session_state.get("username")

        if not username:
            st.error("Please log in to record your mood.")

        elif st.session_state.mg_last_checkin != today:
            try:
                supabase = get_supabase_admin()

                supabase.table("mood_history").insert({
                    "username": username,
                    "mood": mood,
                    "mood_date": today
                }).execute()

                st.session_state.mg_mood_history.append({
                    "date": today,
                    "mood": mood
                })

                st.session_state.mg_last_checkin = today
                add_points(10)

                st.success(
                    "Mood saved successfully! You earned 10 garden points. 🌱"
                )

            except Exception as e:
                st.error(f"Could not save your mood: {e}")

    else:
        st.info("You've already recorded a mood today.")

    st.markdown(
        f'<div class="mg-note">{moods[mood]}</div>',
        unsafe_allow_html=True
    )

    # ---------------- GARDEN DISPLAY ----------------

    st.markdown("## 🌿 Your Little Garden")

    ground_items = []

    decorations = st.session_state.mg_decorations

    for decoration in decorations:
        ground_items.append(
            f'<span class="mg-decoration">{decoration}</span>'
        )

    growth_emojis = {
        0: "🌱",
        1: "🌿",
        2: "🪴",
        3: None
    }

    for plant in st.session_state.mg_plants:
        if plant["growth"] >= 3:
            emoji = plant["emoji"]
        elif plant["growth"] == 0:
            emoji = "🌱"
        else:
            emoji = growth_emojis[plant["growth"]]

        ground_items.append(
            f'<span class="mg-plant" title="Growing plant">{emoji}</span>'
        )

    if not ground_items:
        garden_content = (
            '<div class="mg-empty">'
            '🪴 Your garden is waiting for its first seed!<br>'
            'Plant a flower below to begin your journey.'
            '</div>'
        )
    else:
        garden_content = "".join(ground_items)

    st.markdown(
        f"""
        <div class="mg-ground">
            <div class="mg-ground-title">☀️ A peaceful place to grow</div>
            <div style="padding: 18px 0;">{garden_content}</div>
            <div style="font-size:22px;">🪨 🌿 🦋 🌿 🪨</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- PLANTING ----------------

    st.markdown("## 🌱 Plant Something New")

    seed_names = list(seeds.keys())

    selected_seed = st.selectbox(
        "Choose a seed",
        seed_names,
        format_func=lambda name: (
            f"{name} — Free"
            if seeds[name]["cost"] == 0
            else f"{name} — {seeds[name]['cost']} points"
        ),
        key="mg_selected_seed"
    )

    st.caption(seeds[selected_seed]["description"])

    if st.button(
        "🌱 Plant Seed",
        use_container_width=True,
        key="mg_plant_seed"
    ):
        plant_seed()
        st.rerun()

    # ---------------- WATERING ----------------

    st.markdown("## 💧 Care for Your Plants")

    plants = st.session_state.mg_plants

    if not plants:
        st.info("Plant your first seed before watering.")
    else:
        for index, plant in enumerate(plants):
            col1, col2 = st.columns([3, 1])

            with col1:
                stage = (
                    "🌱 Seedling"
                    if plant["growth"] == 0
                    else "🌿 Growing"
                    if plant["growth"] < 3
                    else plant["emoji"] + " Mature"
                )

                st.markdown(
                    f"**{plant['emoji']} {plant['name']}** — {stage}"
                )

                if plant["watered"]:
                    st.caption("Watered today 💧")
                else:
                    st.caption("Needs a little care.")

            with col2:
                if st.button(
                    "💧 Water",
                    key=f"mg_water_{plant['id']}",
                    disabled=plant["watered"],
                    use_container_width=True
                ):
                    water_plant(index)
                    st.rerun()

    # ---------------- DECORATIONS ----------------

    st.markdown("## 🦋 Garden Decorations")

    decoration_options = {
        "🦋 Butterfly": ("🦋", 15),
        "🌳 Tree": ("🌳", 25),
        "🪷 Lily": ("🪷", 20),
        "🐦 Bird": ("🐦", 30),
    }

    for name, (emoji, cost) in decoration_options.items():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"{emoji} {name} — {cost} points")

        with col2:
            if st.button(
                "Unlock",
                key=f"mg_unlock_{name}",
                use_container_width=True
            ):
                if emoji in st.session_state.mg_decorations:
                    st.info("You've already unlocked this decoration!")
                elif st.session_state.mg_points >= cost:
                    st.session_state.mg_points -= cost
                    st.session_state.mg_decorations.append(emoji)

                    st.session_state.mg_level = (
                        st.session_state.mg_points // 50
                    ) + 1

                    # Save the updated garden
                    save_garden_progress()

                    st.success(f"{emoji} Decoration unlocked!")
                    st.rerun()
                else:
                    st.warning(
                        f"You need {cost} points to unlock this decoration."
                    )

                

    # ---------------- MOOD HISTORY ----------------

    with st.expander("📅 My Mood History"):
        history = st.session_state.mg_mood_history

        if history:
            for entry in reversed(history):
                st.write(f"**{entry['date']}** — {entry['mood']}")
        else:
            st.info("Your mood check-ins will appear here.")

    st.markdown(
        """
        <div class="mg-note">
            💜 Remember: your garden doesn't need to be perfect.
            Every small act of self-care counts.
        </div>
        """,
        unsafe_allow_html=True
    )