from google import genai
import streamlit as st

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

try:
    print("Available Models:\n")

    for model in client.models.list():
        print(model.name)

except Exception as e:
    print(type(e).__name__)
    print(e)