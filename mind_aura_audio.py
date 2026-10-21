import streamlit as st
import tempfile
import os
from google import genai

def transcribe_audio(audio_file):
    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        st.error("GEMINI_API_KEY was not found.")
        return ""

    temp_path = None

    try:
        client = genai.Client(api_key=api_key)

        audio_bytes = audio_file.getvalue()

        if not audio_bytes:
            st.error("The recording contains no audio.")
            return ""

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        audio = client.files.upload(file=temp_path)

        interaction = client.interactions.create(
            model="gemini-3.5-transcribe",
            input=[
                {
                    "type": "audio",
                    "uri": audio.uri,
                    "mime_type": audio.mime_type,
                }
            ],
        )

        if interaction.output_text:
            return interaction.output_text.strip()

        return ""

    except Exception as e:
        st.error(f"Mind Aura transcription error: {e}")
        return ""

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass