from google import genai
import streamlit as st

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

try:
    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents="Say hello in one sentence."
    )

    print("SUCCESS")
    print(response.text)

except Exception as e:
    print("ERROR")
    print(type(e).__name__)
    print(e)