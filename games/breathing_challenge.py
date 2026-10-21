import streamlit as st
import time

def render_breathing_challenge():
    st.markdown(
        """
        <style>
        .breathing-title {
            color: #51418f;
            font-size: 32px;
            font-weight: 800;
            text-align: center;
        }

        .breathing-subtitle {
            color: #74718b;
            text-align: center;
            font-size: 16px;
        }

        .breathing-circle {
            width: 180px;
            height: 180px;
            margin: 25px auto;
            border-radius: 50%;
            background: radial-gradient(
                circle,
                #c4b5fd,
                #a78bfa,
                #818cf8
            );
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 22px;
            font-weight: bold;
            box-shadow: 0 0 35px rgba(167, 139, 250, 0.4);
        }

        .breathing-circle {
            transition: transform 1s ease-in-out;
        }

        .breathing-circle.inhale {
            transform: scale(1.25);
        }

        .breathing-circle.exhale {
            transform: scale(0.8);
        }

        .breathing-circle.hold {
            transform: scale(1);
        }

        .breathing-note {
            background: #f5f3ff;
            padding: 15px;
            border-radius: 12px;
            color: #51418f;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="breathing-title">🌬️ Breathing Challenge</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="breathing-subtitle">'
        'Pause, breathe gently, and give your mind a break.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # ---------------- RELAXATION MODE ----------------

    relaxation_mode = st.selectbox(
        "🧘 What would you like to focus on?",
        [
            "📚 Study Break",
            "😌 Stress Relief",
            "🌙 Bedtime Relaxation",
            "🌿 Mindful Breathing"
        ],
        key="relaxation_mode"
    )

    mode_descriptions = {
        "📚 Study Break":
            "Give your mind a short break between study sessions.",
        "😌 Stress Relief":
            "Slow down and take a comfortable breathing break.",
        "🌙 Bedtime Relaxation":
            "Create a quiet moment before going to sleep.",
        "🌿 Mindful Breathing":
            "Focus gently on your breathing and the present moment."
    }

    st.info(mode_descriptions[relaxation_mode])

    # ---------------- RECOMMENDED SESSION SETTINGS ----------------

    recommended_settings = {
        "📚 Study Break": {
            "pattern": "Balanced Breath — 4-0-4",
            "duration": 1
        },
        "😌 Stress Relief": {
            "pattern": "Relaxing Breath — 4-0-6",
            "duration": 2
        },
            "🌙 Bedtime Relaxation": {
            "pattern": "Relaxing Breath — 4-0-6",
            "duration": 3
        },
        "🌿 Mindful Breathing": {
            "pattern": "Balanced Breath — 4-0-4",
            "duration": 3
        }
    }

    settings = recommended_settings[relaxation_mode]

    pattern_options = [
        "Relaxing Breath — 4-0-6",
        "Balanced Breath — 4-0-4",
        "Box Breathing — 4-4-4-4"
    ]

    duration_options = [1, 2, 3, 5]

    if st.session_state.get("previous_relaxation_mode") != relaxation_mode:
        st.session_state.breathing_pattern = settings["pattern"]
        st.session_state.breathing_duration = settings["duration"]
        st.session_state.previous_relaxation_mode = relaxation_mode

    pattern = st.selectbox(
        "Choose your breathing pattern",
        pattern_options,
        key="breathing_pattern"
    )

    duration = st.selectbox(
        "Session duration",
        duration_options,
        format_func=lambda x: f"{x} minute{'s' if x > 1 else ''}",
        key="breathing_duration"
    )
    with st.expander("🌬️ How to Use the Breathing Challenge", expanded=True):

        st.markdown("""
        ### 🎯 Your Goal
        Take a short, comfortable breathing break to help yourself relax.

        ### 🕹️ How to Play

        **1. Choose your breathing pattern**
        Select the breathing exercise that feels comfortable.

        **2. Select your session duration**
        Start with just one minute if you're new.

        **3. Press ▶ Start**
       Follow the instructions displayed inside the circle.

        **4. Follow each breathing phase**
        - 🌬️ **Inhale gently:** Breathe in comfortably.
        - ⏸️ **Hold comfortably:** Only if comfortable and included in your pattern.
        - 😮‍💨 **Exhale slowly:** Let your breath out gently.

        **5. Pause or restart whenever needed**
        There is no pressure to finish the session.

        ### 💡 Example
        With Relaxing Breath — 4-0-6:
        - Inhale gently for 4 seconds.
        - Exhale slowly for 6 seconds.
        - Repeat at your own comfortable pace.

        **Tip:** Focus on your breath and let go of distractions.
        """)

        st.info(
            "💜 Breathe naturally if you feel uncomfortable, "
            "and stop the exercise if you experience dizziness or distress."
        )

    st.write("")

    if pattern == "Relaxing Breath — 4-0-6":
        phases = [
            ("Inhale gently", 4),
            ("Exhale slowly", 6)
        ]
    elif pattern == "Balanced Breath — 4-0-4":
        phases = [
            ("Inhale gently", 4),
            ("Exhale slowly", 4)
        ]
    else:
        phases = [
            ("Inhale gently", 4),
            ("Hold comfortably", 4),
            ("Exhale slowly", 4),
            ("Hold comfortably", 4)
        ]

    if "breathing_running" not in st.session_state:
        st.session_state.breathing_running = False

    if "breathing_paused" not in st.session_state:
        st.session_state.breathing_paused = False

    if "breathing_started_at" not in st.session_state:
        st.session_state.breathing_started_at = None

    if "breathing_completed" not in st.session_state:
        st.session_state.breathing_completed = False

    if "breathing_elapsed_before_pause" not in st.session_state:
        st.session_state.breathing_elapsed_before_pause = 0.0

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("▶ Start", use_container_width=True):
            st.session_state.breathing_running = True
            st.session_state.breathing_paused = False
            st.session_state.breathing_started_at = time.time()
            st.session_state.breathing_elapsed_before_pause = 0.0
            st.session_state.breathing_completed = False
            st.rerun()

    with col2:
        if st.button(
            "⏸ Pause",
            use_container_width=True,
            disabled=(
                not st.session_state.breathing_running
                or st.session_state.breathing_paused
            )
        ):
            st.session_state.breathing_elapsed_before_pause += (
                time.time() - st.session_state.breathing_started_at
            )
            st.session_state.breathing_paused = True
            st.rerun()

    with col3:
        if st.button("🔄 Restart", use_container_width=True):
            st.session_state.breathing_running = False
            st.session_state.breathing_paused = False
            st.session_state.breathing_started_at = None
            st.session_state.breathing_elapsed_before_pause = 0.0
            st.session_state.breathing_completed = False
            st.rerun()

    if st.session_state.breathing_running and not st.session_state.breathing_paused:
        if st.session_state.breathing_paused:
            elapsed = st.session_state.breathing_elapsed_before_pause
        else:
            elapsed = (
                st.session_state.breathing_elapsed_before_pause
                + time.time() - st.session_state.breathing_started_at
            )

        total_seconds = duration * 60

        if elapsed >= total_seconds:
            st.session_state.breathing_running = False
            st.session_state.breathing_paused = False
            st.session_state.breathing_completed = True
            st.session_state.breathing_elapsed_before_pause = 0.0

            st.success(
                "🌸 Wonderful! You completed your breathing session."
            )
            st.balloons()

        else:
            elapsed = max(0, elapsed)
            remaining = max(0, int(total_seconds - elapsed))

            cycle_duration = sum(seconds for _, seconds in phases)
            position = elapsed % cycle_duration

            current_phase = phases[-1][0]
            phase_remaining = 0

            for phase_name, phase_seconds in phases:
                if position < phase_seconds:
                    current_phase = phase_name
                    phase_remaining = phase_seconds - position
                    break
                position -= phase_seconds

            cycle_count = int(elapsed // cycle_duration)

            # Choose animation state for the current breathing phase
            if "Inhale" in current_phase:
                animation_class = "inhale"
            elif "Exhale" in current_phase:
                animation_class = "exhale"
            else:
                animation_class = "hold"

            st.markdown(
                f"""
                <div class="breathing-circle {animation_class}">
                    <div>
                        {current_phase}<br>
                        {max(1, int(phase_remaining))} sec
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            metric1, metric2 = st.columns(2)

            metric1.metric(
                "⏱️ Time Remaining",
                f"{remaining // 60:02d}:{remaining % 60:02d}"
            )

            metric2.metric(
                "🔄 Completed Cycles",
                cycle_count
            )

            st.progress(min(elapsed / total_seconds, 1.0))

            if not st.session_state.breathing_paused:
                time.sleep(1)
                st.rerun()

    if st.session_state.breathing_paused:
        st.info("Your session is paused. Resume when you're ready.")

        if st.button("▶ Resume", use_container_width=True):
            st.session_state.breathing_started_at = time.time()
            st.session_state.breathing_paused = False
            st.rerun()

    elif st.session_state.breathing_completed:
        st.success(
            "🌸 Session completed! Take a moment to notice how you feel."
        )

    else:
        st.info("Press Start when you're ready to begin.")