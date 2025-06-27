import streamlit as st
import requests
from googletrans import Translator

# Streamlit UI setup
st.set_page_config(page_title="MediGuide Assistant", page_icon="🩺")
st.title("🩺 MediGuide: Your Medical AI Assistant")

st.markdown("""
Welcome to MediGuide — a powerful AI medical assistant powered by Hugging Face's Mixtral model.
Ask your question in **any language**, and the assistant will respond in that language.
""")

# Translator setup
translator = Translator()

# Input field
user_input = st.text_input("Ask a medical question (in any language):")

if user_input:
    with st.spinner("Translating and getting response..."):
        try:
            # Detect input language
            detected_lang = translator.detect(user_input).lang

            # Translate input to English
            translated_input = translator.translate(user_input, src=detected_lang, dest='en').text

            # Hugging Face API call
            url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
            headers = {
                "Authorization": f"Bearer {st.secrets['hf_token']}",
                "Content-Type": "application/json"
            }
            payload = {"inputs": f"[INST] {translated_input} [/INST]"}
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                english_reply = result[0].get("generated_text", "⚠️ No reply received.")

                # Translate output back to original language
                final_reply = translator.translate(english_reply, src='en', dest=detected_lang).text

                st.success(final_reply)
            else:
                st.error(f"❌ Error {response.status_code}:\n{response.text}")

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
