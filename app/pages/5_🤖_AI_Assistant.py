"""
TrafficIQ - Mistral AI Traffic Assistant Interface
Interactive chatbot powered by Mistral AI Cloud LLM providing traffic intelligence explanations,
congestion root-cause diagnostics, signal timing recommendations, and alternate route diversion suggestions.
"""

import streamlit as st
import requests
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from configs.config import MISTRAL_API_KEY, MISTRAL_API_URL, MISTRAL_MODEL
from database.database import TrafficDatabase
from utils.ui import apply_custom_css, render_header

st.set_page_config(page_title="TrafficIQ - Mistral AI Assistant", page_icon="🤖", layout="wide")

apply_custom_css()
render_header("Mistral AI Traffic Assistant", "Ask context-aware traffic questions, signal timing optimization, and alternate route diversion suggestions powered by Mistral AI Cloud LLM", "🤖")

db = TrafficDatabase()
sessions = db.get_all_sessions(include_empty=False)

# Secure API Key loading without rendering key text on screen
api_key = st.session_state.get("mistral_api_key") or MISTRAL_API_KEY

# Sidebar Configuration
st.sidebar.header("Mistral AI Configuration")
model_name = st.sidebar.selectbox("Mistral Model", ["mistral-small-latest", "mistral-medium-latest", "open-mistral-7b"])

if api_key:
    st.sidebar.success("🔒 Mistral API Connected (Private Key Active)")
else:
    st.sidebar.error("⚠️ Mistral API Key not set. Configure `MISTRAL_API_KEY` in environment `.env` file.")

# Context Session Selection
selected_session = None
if sessions:
    session_options = ["None (General Traffic Knowledge)"] + [s["session_id"] for s in sessions]
    selected_sid = st.selectbox("Select Traffic Session Context for AI Assistant", session_options)
    if selected_sid != "None (General Traffic Knowledge)":
        selected_session = db.get_session_details(selected_sid)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your **Mistral AI Traffic Assistant**. Select a session context above and ask me about congestion root causes, signal green timing splits, alternate route diversions, or emissions!"
        }
    ]

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def query_mistral_api(prompt: str, session: dict = None, api_key: str = "") -> str:
    """Calls Mistral AI API with traffic context."""
    system_context = (
        "You are TrafficIQ AI Assistant, an expert AI traffic analyst powering a smart city traffic management platform. "
        "You perform congestion-aware route optimization by assigning dynamic weights to monitored road corridors using "
        "real-time traffic density, congestion index, heavy vehicle composition, and queue length. Based on these weighted scores, "
        "you recommend lower-congestion alternative corridors to assist traffic operators in diversion planning. "
        "You also optimize traffic signal green timing splits based on weighted Road Load (Cars=1, Motorcycles=0.5, Buses=3, Trucks=4). "
        "Respond concisely, accurately, and professionally in Markdown format."
    )

    if session:
        system_context += f"\n\nCURRENT SESSION CONTEXT:\n" \
                           f"- Session ID: {session.get('session_id')}\n" \
                           f"- Total Vehicles Counted: {session.get('total_vehicles_counted')}\n" \
                           f"- Peak Density: {session.get('peak_density')}\n" \
                           f"- Avg Congestion Index: {session.get('avg_congestion_score', 0):.1f} / 100\n" \
                           f"- Peak Vehicles Present: {session.get('peak_vehicles_present')}\n" \
                           f"- Total CO2 Emissions: {session.get('total_co2_g', 0):.1f} g"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_context},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }

    try:
        res = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=12)
        if res.status_code == 200:
            data = res.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"⚠️ Mistral API Error ({res.status_code}): {res.text}"
    except Exception as e:
        return f"⚠️ Connection error reaching Mistral API: {e}"

# User Chat Input
if prompt := st.chat_input("Ask Mistral AI about traffic conditions, signal timing, or route diversions..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Mistral AI is analyzing traffic intelligence..."):
        if api_key:
            response_text = query_mistral_api(prompt, selected_session, api_key)
        else:
            response_text = "⚠️ **Mistral API Key missing.** Please add `MISTRAL_API_KEY=your_key` in the platform `.env` configuration file."

    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})

st.sidebar.markdown("### 🤖 Mistral AI Assistant")
st.sidebar.info("Consult Mistral AI for traffic diagnostics, green timing optimizations, and route diversion recommendations.")
