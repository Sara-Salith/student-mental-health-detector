from google import genai
import streamlit as st
import time


# ============================================================
# FALLBACK WELLNESS ANALYSIS
# ============================================================

def get_fallback_analysis(prediction):

    if prediction == "Higher Mental Health Risk":

        return """
### 1. What This Prediction Means

Your responses indicate a higher estimated mental health risk based on the screening model. This result is only an AI-based screening estimate and does not mean that you have a mental health condition.

### 2. Main Contributing Factors

The prediction is based on patterns identified in the information provided during your assessment. Academic pressure, work or study demands, sleep, financial stress, lifestyle habits, and other wellbeing indicators can influence the screening result.

### 3. Practical Wellness Suggestions

- Try to maintain a consistent sleep schedule and aim for sufficient rest.
- Break large academic tasks into smaller, manageable goals.
- Take short breaks during long study sessions.
- Make time for physical activity, relaxation, hobbies, or activities you enjoy.
- Talk with someone you trust if you feel overwhelmed or under pressure.

### 4. When to Consider Reaching Out for Support

If stress, low mood, anxiety, sleep difficulties, or feelings of being overwhelmed continue or interfere with your daily life, consider talking to a trusted person, counselor, or qualified mental-health professional.

If you ever feel that you may be in immediate danger or might harm yourself, seek urgent help from local emergency services or a qualified professional.
"""

    else:

        return """
### 1. What This Prediction Means

Your responses indicate a lower estimated mental health risk based on the screening model. This is an AI-based screening estimate and does not represent a medical diagnosis.

### 2. Main Contributing Factors

The information provided during your assessment suggests several relatively balanced wellbeing indicators. Maintaining healthy academic, lifestyle, and personal routines can continue supporting your overall wellbeing.

### 3. Practical Wellness Suggestions

- Continue maintaining a regular sleep routine.
- Keep a healthy balance between studying, relaxation, and personal activities.
- Stay physically active through walking, exercise, or activities you enjoy.
- Maintain supportive relationships with friends, family, or people you trust.
- Make time for relaxation and activities that help you recharge.

### 4. When to Consider Reaching Out for Support

Even when a screening result indicates lower risk, mental wellbeing can change over time. If you begin experiencing persistent stress, anxiety, low mood, sleep problems, or difficulty managing daily responsibilities, consider speaking with a trusted person, counselor, or qualified mental-health professional.
"""


# ============================================================
# GEMINI AI ANALYSIS
# ============================================================

def get_ai_analysis(student_data, prediction):

    # --------------------------------------------------------
    # GET API KEY
    # --------------------------------------------------------

    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:

        return get_fallback_analysis(prediction)


    # --------------------------------------------------------
    # CREATE GEMINI CLIENT
    # --------------------------------------------------------

    client = genai.Client(
        api_key=api_key
    )


    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are an AI wellness assistant for a Student Mental Health Detector.

The machine learning model predicted:

{prediction}

Student assessment data:

{student_data}

Provide a supportive, simple and personalized wellness analysis.

Use exactly these four sections:

### 1. What This Prediction Means

Explain what the screening result means in simple language.

### 2. Main Contributing Factors

Explain the important patterns in the assessment that may have influenced the result.

Do not unnecessarily repeat sensitive information.

### 3. Practical Wellness Suggestions

Provide 3 to 5 realistic and practical suggestions.

### 4. When to Consider Reaching Out for Support

Explain when the student may benefit from talking to a trusted person,
counselor, or qualified mental-health professional.

Important rules:

- This is an AI-based screening result, NOT a medical diagnosis.
- Never diagnose the student.
- Never claim certainty.
- Use supportive and non-judgmental language.
- Do not use alarming language unnecessarily.
- Do not shame or blame the student.
- Keep the response concise and useful.
"""


    # --------------------------------------------------------
    # TRY GEMINI
    # --------------------------------------------------------

    for attempt in range(2):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            if response and response.text:

                return response.text.strip()


        except Exception:

            # If the first attempt fails, wait briefly
            # and try once more.
            if attempt == 0:

                time.sleep(2)

            else:

                pass


    # --------------------------------------------------------
    # GEMINI FAILED
    # USE BUILT-IN FALLBACK
    # --------------------------------------------------------

    return get_fallback_analysis(prediction)