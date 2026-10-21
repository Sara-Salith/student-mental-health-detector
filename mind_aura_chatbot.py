import streamlit as st
import base64
from google import genai
from components.history import get_user_history
import tempfile
import os
import traceback
import pandas as pd
from mind_aura_audio import transcribe_audio


# ==================================================
# CHAT SESSION KEY
# ==================================================

CHAT_KEY = "mind_aura_messages"


# ==================================================
# GET EXISTING ASSESSMENT HISTORY
# ==================================================

def _get_history():

    username = st.session_state.get(
        "username",
        ""
    )

    if not username:
        return None

    try:

        return get_user_history(username)

    except Exception:

        return None


# ==================================================
# BUILD STUDENT CONTEXT
# ==================================================

def _build_context():

    username = st.session_state.get(
        "username",
        ""
    )

    current = st.session_state.get(
        "assessment_data",
        {}
    )

    prediction = st.session_state.get(
        "prediction"
    )

    risk_score = st.session_state.get(
        "risk_score"
    )

    history = _get_history()

    comparison = _build_history_comparison(history)

    # --------------------------------------------------
    # CURRENT ASSESSMENT
    # --------------------------------------------------

    # If the current assessment is already available
    # in the current session, use it.
    #
    # Otherwise, use the latest assessment from
    # Supabase history as the current assessment.
    if not current and history is not None and not history.empty:

        latest = history.iloc[0]

        current = {
            "Gender": latest.get("gender"),
            "Age": latest.get("age"),
            "Academic Pressure": latest.get(
                "academic_pressure"
            ),
            "Work Pressure": latest.get(
                "work_pressure"
            ),
            "CGPA": latest.get("cgpa"),
            "Study Satisfaction": latest.get(
                "study_satisfaction"
            ),
            "Job Satisfaction": latest.get(
                "job_satisfaction"
            ),
            "Sleep Duration": latest.get(
                "sleep_duration"
            ),
            "Dietary Habits": latest.get(
                "dietary_habits"
            ),
            "Work/Study Hours": latest.get(
                "work_study_hours"
            ),
            "Financial Stress": latest.get(
                "financial_stress"
            ),
            "Family History": latest.get(
                "family_history"
            )
        }

        prediction = latest.get(
            "prediction"
        )

        risk_score = latest.get(
            "risk_score"
        )

    # --------------------------------------------------
    # BASE CONTEXT
    # --------------------------------------------------

    context = {

        "username": username,

        "current_assessment": current,

        "current_prediction": prediction,

        "current_risk_score": risk_score,

        "assessment_changes": comparison,

        "assessment_factors": {
        "Gender": current.get("Gender"),
        "Age": current.get("Age"),
        "Academic Pressure": current.get("Academic Pressure"),
        "Work Pressure": current.get("Work Pressure"),
        "CGPA": current.get("CGPA"),
        "Study Satisfaction": current.get("Study Satisfaction"),
        "Job Satisfaction": current.get("Job Satisfaction"),
        "Sleep Duration": current.get("Sleep Duration"),
        "Dietary Habits": current.get("Dietary Habits"),
        "Work/Study Hours": current.get("Work/Study Hours"),
        "Financial Stress": current.get("Financial Stress"),
        "Family History": current.get("Family History")
    }

    }

    # --------------------------------------------------
    # RECENT ASSESSMENT HISTORY
    # --------------------------------------------------

    if history is not None and not history.empty:

        selected_columns = [

            "timestamp",
            "prediction",
            "risk_score",
            "gender",
            "age",
            "academic_pressure",
            "work_pressure",
            "cgpa",
            "study_satisfaction",
            "job_satisfaction",
            "sleep_duration",
            "dietary_habits",
            "work_study_hours",
            "financial_stress",
            "family_history",

        ]

        available = [

            column
            for column in selected_columns
            if column in history.columns

        ]

        recent = history[
            available
        ].head(5).copy()

        if "timestamp" in recent.columns:

            recent["timestamp"] = (
                recent["timestamp"]
                .astype(str)
            )

        context[
            "recent_assessment_history"
        ] = recent.to_dict(
            orient="records"
        )

    else:

        context[
            "recent_assessment_history"
        ] = []

    return context


# ==================================================
# COMPARE RECENT ASSESSMENTS
# ==================================================

def _build_history_comparison(history):

    if history is None or history.empty:
        return {}

    # We need at least two assessments to compare
    if len(history) < 2:
        return {}

    # History is already sorted newest first
    current = history.iloc[0]
    previous = history.iloc[1]

    comparison = {}

    # --------------------------------------------------
    # RESULT / RISK SCORE
    # --------------------------------------------------

    if (
        "risk_score" in history.columns
        and pd.notna(current.get("risk_score"))
        and pd.notna(previous.get("risk_score"))
    ):

        current_risk = float(
            current.get("risk_score")
        )

        previous_risk = float(
            previous.get("risk_score")
        )

        risk_change = current_risk - previous_risk

        comparison["risk_score"] = {
            "previous": round(previous_risk, 2),
            "current": round(current_risk, 2),
            "change": round(risk_change, 2)
        }

    # --------------------------------------------------
    # FACTORS TO COMPARE
    # --------------------------------------------------

    factor_columns = {

        "Academic Pressure":
            "academic_pressure",

        "Work Pressure":
            "work_pressure",

        "CGPA":
            "cgpa",

        "Study Satisfaction":
            "study_satisfaction",

        "Job Satisfaction":
            "job_satisfaction",

        "Work/Study Hours":
            "work_study_hours",

        "Financial Stress":
            "financial_stress"

    }

    factor_changes = {}

    for label, column in factor_columns.items():

        if column not in history.columns:
            continue

        current_value = current.get(column)
        previous_value = previous.get(column)

        if (
            pd.isna(current_value)
            or pd.isna(previous_value)
        ):
            continue

        try:

            current_value = float(
                current_value
            )

            previous_value = float(
                previous_value
            )

            change = current_value - previous_value

            if change > 0:
                direction = "increased"

            elif change < 0:
                direction = "decreased"

            else:
                direction = "unchanged"

            factor_changes[label] = {
                "previous": previous_value,
                "current": current_value,
                "change": round(change, 2),
                "direction": direction
            }

        except (ValueError, TypeError):

            continue

    comparison["factor_changes"] = factor_changes

    # --------------------------------------------------
    # CATEGORICAL CHANGES
    # --------------------------------------------------

    categorical_columns = {

        "Sleep Duration":
            "sleep_duration",

        "Dietary Habits":
            "dietary_habits",

        "Gender":
            "gender",

        "Family History":
            "family_history"

    }

    categorical_changes = {}

    for label, column in categorical_columns.items():

        if column not in history.columns:
            continue

        current_value = current.get(column)
        previous_value = previous.get(column)

        if (
            pd.isna(current_value)
            or pd.isna(previous_value)
        ):
            continue

        if str(current_value) != str(previous_value):

            categorical_changes[label] = {
                "previous": str(previous_value),
                "current": str(current_value)
            }

    comparison[
        "categorical_changes"
    ] = categorical_changes

    # --------------------------------------------------
    # PREDICTION CHANGE
    # --------------------------------------------------

    if "prediction" in history.columns:

        previous_prediction = previous.get(
            "prediction"
        )

        current_prediction = current.get(
            "prediction"
        )

        if (
            pd.notna(previous_prediction)
            and pd.notna(current_prediction)
            and str(previous_prediction)
            != str(current_prediction)
        ):

            comparison[
                "prediction_change"
            ] = {
                "previous":
                    str(previous_prediction),

                "current":
                    str(current_prediction)
            }

    return comparison

# ==================================================
# GET GEMINI RESPONSE
# ==================================================
def _get_reply(user_message):
    """
    Generate a Mind Aura response using Gemini with model fallback.
    """

    import time

    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        return (
            "I'm unable to connect to the AI service right now. "
            "Please try again later."
        )

    client = genai.Client(api_key=api_key)

    messages = st.session_state.get(CHAT_KEY, [])

    # Keep recent conversation context small to reduce token usage.
    recent_chat = messages[-6:]

    context = _build_context()

    prompt = f"""
You are Mind Aura, a friendly AI wellness chatbot
inside a Student Mental Health Detector application.

Your role is to:
- Listen to the student.
- Explain their existing screening information when relevant.
- Help them understand assessment history when asked.
- Provide general wellness support.
- Continue conversations naturally.

IMPORTANT RULES:

1. Screening results are NOT medical diagnoses.
2. Never diagnose a mental-health condition.
3. Never claim certainty about the student's mental health.
4. Do not judge, shame, frighten, or blame the student.
5. Do not unnecessarily repeat sensitive assessment information.
6. Do not invent information that is not provided.
7. Keep responses conversational and reasonably concise.
8. If discussing an assessment result, describe it as an
   AI-based screening estimate.
9. If discussing assessment changes over time, use the
   available assessment history.
10. Do not expose unrelated private information.
11. For urgent safety situations, encourage the student
    to contact a trusted adult/person and appropriate
    local emergency or professional support.
12. Do not provide instructions for self-harm or dangerous behaviour.
13. Do not pretend to be a doctor, therapist, counsellor,
    or other medical professional.

STUDENT CONTEXT:

{context}

RECENT CONVERSATION:

{recent_chat}

NEW USER MESSAGE:

{user_message}
"""

    # Primary model followed by fallback models.
    models = [
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
    ]

    last_error = None

    for model in models:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            if response and response.text:
                return response.text.strip()

            last_error = f"{model} returned an empty response."

        except Exception as e:
            last_error = e
            error_text = str(e).lower()

            temporary_error = (
                "429" in error_text
                or "resource exhausted" in error_text
                or "rate limit" in error_text
                or "503" in error_text
                or "service unavailable" in error_text
                or "deadline exceeded" in error_text
                or "timeout" in error_text
            )

            # For temporary failures, move to the next model.
            # We don't repeatedly hammer the same unavailable model.
            if temporary_error:
                time.sleep(1)
                continue

            # For other errors, stop and expose the actual problem
            # during testing.
            return f"Mind Aura error: {e}"

    return f"Mind Aura error: {last_error}"
# ==================================================
# PROCESS CHAT INPUT
# ==================================================

def _process_message(message_value):

    if message_value is None:
        return

    user_message = ""

    # ----------------------------------------------
    # TEXT INPUT
    # ----------------------------------------------

    if hasattr(message_value, "text"):

        if message_value.text:

            user_message = (
                message_value.text.strip()
            )

    # ----------------------------------------------
    # AUDIO INPUT
    # ----------------------------------------------

    audio_file = None

    if hasattr(message_value, "audio"):

        audio_file = message_value.audio

    # ----------------------------------------------
    # IF AUDIO WAS USED
    # ----------------------------------------------

    if audio_file is not None:

        with st.spinner(
            "Mind Aura is transcribing..."
        ):

            transcript = transcribe_audio(
                audio_file
            )

        if transcript:

            user_message = transcript

        else:

            st.warning(
                "I couldn't transcribe the recording. "
                "Please try again."
            )

            return

    # ----------------------------------------------
    # EMPTY MESSAGE
    # ----------------------------------------------

    if not user_message:
        return

    # ----------------------------------------------
    # SAVE USER MESSAGE
    # ----------------------------------------------

    st.session_state[
        CHAT_KEY
    ].append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    # ----------------------------------------------
    # GET MIND AURA RESPONSE
    # ----------------------------------------------

    with st.spinner(
        "Mind Aura is thinking..."
    ):

        try:

            reply = _get_reply(
                user_message
            )

        except Exception as e:
            st.error(f"Mind Aura error: {type(e).__name__}: {e}")
            print("===== MIND AURA ERROR =====")
            traceback.print_exc()
            print("===========================")

            reply = (
                "I'm having trouble connecting "
                "right now. Please try again "
                "in a moment."
            )

    # ----------------------------------------------
    # SAVE RESPONSE
    # ----------------------------------------------

    st.session_state[
        CHAT_KEY
    ].append(
        {
            "role": "assistant",
            "content": reply,
        }
    )


# ==================================================
# RENDER MIND AURA CHATBOT
# ==================================================

# Load Mind Aura animation from the assets folder
MIND_AURA_GIF_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "mind_aura.gif"
)

with open(MIND_AURA_GIF_PATH, "rb") as gif_file:
    MIND_AURA_GIF = base64.b64encode(gif_file.read()).decode("utf-8")

MIND_AURA_GIF_URI = "data:image/gif;base64," + MIND_AURA_GIF

def _get_static_avatar_path():
    """Create a temporary PNG avatar for Streamlit's chat-message avatar."""
    import base64
    import tempfile
    from PIL import Image
    from io import BytesIO

    cache_key = "mind_aura_static_avatar_path"
    existing = st.session_state.get(cache_key)
    if existing and os.path.exists(existing):
        return existing

    gif_bytes = base64.b64decode(MIND_AURA_GIF)
    image = Image.open(BytesIO(gif_bytes)).convert("RGBA")
    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    )
    image.save(temp.name, format="PNG")
    temp.close()
    st.session_state[cache_key] = temp.name
    return temp.name


def render_mind_aura_chatbot():
    if not st.session_state.get(
        "logged_in",
        False
    ):
        return

    if CHAT_KEY not in st.session_state:
        st.session_state[CHAT_KEY] = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I'm Mind Aura.\n\n"
                    "I'm here to listen, support, and help you "
                    "understand your wellness information. "
                    "How can I help you today?"
                ),
            }
        ]

    # ==================================================
    # ANIMATED MIND AURA STYLING
    # ==================================================
    # Load Mind Aura CSS from the assets folder
    css_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "assets",
        "mind_aura.css"
    )

    with open(css_path, "r", encoding="utf-8") as css_file:
        mind_aura_css = css_file.read()

    # Pass the GIF URI to the external CSS file
    mind_aura_css = mind_aura_css.replace(
        "var(--mind-aura-gif)",
        f'url("{MIND_AURA_GIF_URI}")'
    )

    st.markdown(
        f"""
        <style>
        {mind_aura_css}
        </style>
        """,
        unsafe_allow_html=True,
    )
    # ==================================================
    # FLOATING CHATBOT
    # ==================================================
    with st.popover(
        "\u200b",
        key="mind_aura_launcher",
        type="secondary",
        width=390,
    ):
        st.markdown(
            f"""
<div class="mind-aura-header-row">
    <div class="mind-aura-animated-header">
        <img src="{MIND_AURA_GIF_URI}" alt="Mind Aura" />
    </div>
    <div>
        <div class="mind-aura-name">Mind Aura</div>
        <div class="mind-aura-online">● Online</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        avatar_path = _get_static_avatar_path()

        for message in st.session_state[CHAT_KEY]:
            if message["role"] == "assistant":
                with st.chat_message(
                    "assistant",
                    avatar=avatar_path
                ):
                    st.write(message["content"])
            else:
                with st.chat_message("user"):
                    st.write(message["content"])

        message_value = st.chat_input(
            "Message Mind Aura...",
            key="mind_aura_chat_input",
            accept_audio=True,
            audio_sample_rate=16000,
        )

        if message_value is not None:
            _process_message(message_value)
            st.rerun()
