from google import genai
import streamlit as st


def get_ai_analysis(student_data, prediction):

    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an AI wellness assistant for a Student Mental Health Detector.

The machine learning model predicted:
{prediction}

Student assessment data:
{student_data}

Analyze the result in a supportive and simple way.

Provide:

1. A short explanation of what the prediction means.
2. The main factors in the student's responses that may be contributing to the result.
3. 3 to 5 practical wellness suggestions.
4. When the student should consider talking to a trusted person,
   counselor, or qualified mental-health professional.

Important:
- This is an AI-based screening result, NOT a medical diagnosis.
- Do not make medical diagnoses.
- Do not make claims of certainty.
- Use supportive and non-judgmental language.
- Do not unnecessarily repeat sensitive information.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text