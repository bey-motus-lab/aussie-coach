import streamlit as st
import google.generativeai as genai
import edge_tts
import asyncio
import os

# --- APP CONFIG ---
st.set_page_config(page_title="Aussie AI Coach", layout="wide")

# Setup Gemini (Uses Streamlit Secrets)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# --- VOICE CONFIG ---
# Natasha is a great native Australian voice
VOICE = "en-AU-NatashaNeural"

async def text_to_speech(text, output_file):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

# --- SIDEBAR UI ---
with st.sidebar:
    st.title("🦘 Session Controls")
    register = st.radio("Register:", ["WORKPLACE", "ACADEMIC"])
    scenario = st.text_input("Scenario:", "Defending methodology in a viva")
    if st.button("Reset Session"):
        st.session_state.history = []
        st.rerun()

# --- CHAT STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MAIN UI ---
st.title("Advanced Aussie AI Speaking Coach")

for turn in st.session_state.history:
    st.chat_message("user").write(turn["user"])
    st.chat_message("assistant").write(turn["ai"])

if prompt := st.chat_input("Your performance turn:"):
    st.chat_message("user").write(prompt)
    
    # 1. Gemini Generation
    system_prompt = f"""You are an advanced English speaking coach. Context: {register}. Scenario: {scenario}.
    Be demanding and precise. Provide: 1. Strongest move, 2. Highest-leverage upgrade, 3. Native-like rewrite.
    Then ask the next simulation question."""
    
    response = model.generate_content(f"{system_prompt}\n\nUser: {prompt}")
    ai_text = response.text
    
    st.chat_message("assistant").write(ai_text)
    
    # 2. Edge-TTS Generation
    output_path = "response.mp3"
    # We use asyncio.run because Streamlit is synchronous
    asyncio.run(text_to_speech(ai_text, output_path))
    st.audio(output_path, format="audio/mp3")
    
    st.session_state.history.append({"user": prompt, "ai": ai_text})
