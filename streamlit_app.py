{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 HelveticaNeue;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww21700\viewh13840\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import google.generativeai as genai\
from melo.api import TTS\
import os\
\
# --- APP CONFIG & INIT ---\
st.set_page_config(page_title="Aussie AI Coach", layout="wide")\
\
# Setup Gemini (Uses Streamlit Secrets)\
genai.configure(api_key=st.secrets["
\f1\fs26 AQ.Ab8RN6IlvjVSZqC-uAqKmno0bdB-iPViim_ab2QrGIgyzVuZtQ
\f0\fs24 "])\
model = genai.GenerativeModel('gemini-2.5-pro')\
\
# Setup MeloTTS (Cached to prevent reload on every click)\
@st.cache_resource\
def load_tts():\
    tts = TTS(language='EN', device='cpu')\
    speaker_ids = tts.hps.data.spk2id\
    # Select the Australian speaker\
    aussie_id = speaker_ids.get('EN-AU', list(speaker_ids.values())[0])\
    return tts, aussie_id\
\
tts_model, aussie_id = load_tts()\
\
# --- SIDEBAR UI ---\
with st.sidebar:\
    st.title("\uc0\u55358 \u56728  Session Controls")\
    register = st.radio("Register:", ["WORKPLACE", "ACADEMIC"])\
    scenario = st.text_input("Scenario:", "Defending methodology in a viva")\
    if st.button("Reset Session"):\
        st.session_state.history = []\
        st.rerun()\
\
# --- CHAT STATE ---\
if "history" not in st.session_state:\
    st.session_state.history = []\
\
# --- MAIN UI ---\
st.title("Advanced Aussie AI Speaking Coach")\
\
# Display previous turns\
for turn in st.session_state.history:\
    st.chat_message("user").write(turn["user"])\
    st.chat_message("assistant").write(turn["ai"])\
\
# Chat Input\
if prompt := st.chat_input("Your performance turn:"):\
    st.chat_message("user").write(prompt)\
    \
    # 1. Generate text with Gemini 2.5 Pro\
    system_prompt = f"""You are an advanced English speaking coach. Context: \{register\}. Scenario: \{scenario\}.\
    Be demanding and precise. Provide: 1. Strongest move, 2. Highest-leverage upgrade, 3. Native-like rewrite.\
    Then ask the next simulation question."""\
    \
    response = model.generate_content(f"\{system_prompt\}\\n\\nUser: \{prompt\}")\
    ai_text = response.text\
    \
    # 2. Display text\
    st.chat_message("assistant").write(ai_text)\
    \
    # 3. Generate Audio with MeloTTS\
    output_path = "response.wav"\
    tts_model.tts_to_file(ai_text, aussie_id, output_path, speed=1.0)\
    st.audio(output_path, format="audio/wav")\
    \
    # Save history\
    st.session_state.history.append(\{"user": prompt, "ai": ai_text\})}