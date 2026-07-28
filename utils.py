import pickle
import numpy as np
from google import genai
import streamlit as st
import re

# -----------------------------
# Load ML Model
# -----------------------------

model = pickle.load(open("mental_health_model.pkl", "rb"))

# -----------------------------
# Gemini Client
# -----------------------------

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# -----------------------------
# Encoding Function
# -----------------------------

def encode_data(data):

    gender = 0 if data["gender"] == "Male" else 1

    sleep_map = {
        "Less than 5 hours": 0,
        "5-6 hours": 1,
        "7-8 hours": 2,
        "More than 8 hours": 3
    }

    diet_map = {
        "Unhealthy": 0,
        "Moderate": 1,
        "Healthy": 2
    }

    suicidal = 1 if data["suicidal_thoughts"] == "Yes" else 0

    family = 1 if data["family_history"] == "Yes" else 0

    encoded = np.array([[
        gender,
        data["age"],
        data["academic_pressure"],
        0,
        data["cgpa"],
        data["study_satisfaction"],
        0,
        sleep_map[data["sleep_duration"]],
        diet_map[data["dietary_habits"]],
        suicidal,
        data["study_hours"],
        data["financial_stress"],
        family
    ]])

    return encoded

# -----------------------------
# Prediction
# -----------------------------

def predict(data):

    encoded = encode_data(data)

    prediction = model.predict(encoded)[0]

    try:

        probability = model.predict_proba(encoded)[0][1]

    except:

        probability = 1 if prediction == 1 else 0

    return prediction, probability

# -----------------------------
# Gemini Recommendation
# -----------------------------

def ai_recommendation(data, prediction):

    status = "High Risk" if prediction == 1 else "Low Risk"

    prompt = f"""
You are a student wellness expert.

Student Details:

Gender : {data['gender']}
Age : {data['age']}
CGPA : {data['cgpa']}
Academic Pressure : {data['academic_pressure']}
Study Satisfaction : {data['study_satisfaction']}
Study Hours : {data['study_hours']}
Sleep : {data['sleep_duration']}
Diet : {data['dietary_habits']}
Financial Stress : {data['financial_stress']}
Family History : {data['family_history']}
Suicidal Thoughts : {data['suicidal_thoughts']}

Prediction : {status}

Return your response in Markdown using the following headings:

# 🌟 Encouragement

# 📚 Study Advice

# 💤 Sleep Recommendations

# 🥗 Nutrition

# 🧘 Stress Management

# 💬 Emotional Support

# 💪 Daily Motivation

Keep the tone supportive, encouraging, and easy to understand.

Limit the response to about 200 words.

Do not diagnose the student.

Avoid repeating the prediction.

Focus on practical, personalized suggestions.
"""
    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt
    )

    return response.text
