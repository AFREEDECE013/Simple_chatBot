import streamlit as st
# from google import genai
import google.genai as genai
import os
from dotenv import load_dotenv

# -------------------------------
# CONFIG
# -------------------------------
SYSTEM_PROMPT = "You are a helpful AI assistant. Answer clearly and concisely."
MAX_HISTORY = 10

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
google_model = os.getenv("GOOGLE_MODEL")

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI Chat", layout="wide")

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
.chat-container {
    max-width: 800px;
    margin: auto;
}

.user-msg {
    background-color: #6366f1;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 5px 0;
    color: white;
    text-align: right;
}

.bot-msg {
    background-color: #1e293b;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 5px 0;
    color: white;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"
    st.session_state.chats["Chat 1"] = []

# -------------------------------
# SIDEBAR (CHATGPT STYLE)
# -------------------------------
st.sidebar.title("💬 Chats")

# New Chat Button
if st.sidebar.button("➕ New Chat"):
    new_chat_name = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat_name] = []
    st.session_state.current_chat = new_chat_name

st.sidebar.markdown("---")

# Chat List
for chat_name in st.session_state.chats.keys():
    if chat_name == st.session_state.current_chat:
        st.sidebar.markdown(f"👉 **{chat_name}**")
    else:
        if st.sidebar.button(chat_name):
            st.session_state.current_chat = chat_name

# -------------------------------
# MAIN HEADER
# -------------------------------
st.title("💬 AI Assistant")

# -------------------------------
# FUNCTION: GET RESPONSE
# -------------------------------
def get_response():
    conversation = SYSTEM_PROMPT + "\n\n"

    current_chat = st.session_state.chats[st.session_state.current_chat]
    recent_history = current_chat[-MAX_HISTORY:]

    for role, msg in recent_history:
        if role == "user":
            conversation += f"User: {msg}\n"
        else:
            conversation += f"Assistant: {msg}\n"

    response = client.models.generate_content(
        model=google_model,
        contents=conversation
    )

    return response.text if response.text else "⚠️ No response"

# -------------------------------
# DISPLAY CHAT
# -------------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

current_chat = st.session_state.chats[st.session_state.current_chat]

for role, message in current_chat:
    if role == "user":
        st.markdown(f'<div class="user-msg">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{message}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# INPUT
# -------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    current_chat.append(("user", user_input))

    bot_response = get_response()

    current_chat.append(("assistant", bot_response))

    st.rerun()
