import streamlit as st
import google.generativeai as genai
import sqlite3
from dotenv import load_dotenv
import os

# -------------------------------
# CONFIG
# -------------------------------
SYSTEM_PROMPT = "You are a helpful AI assistant. Answer clearly and concisely."
MAX_HISTORY = 10

# -------------------------------
# LOAD ENV (LOCAL)
# -------------------------------
load_dotenv()

api_key = None

# Try Streamlit secrets (only if exists)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = os.getenv("GOOGLE_API_KEY")

# Final check
if not api_key:
    st.error("❌ API key not found. Add it in .env (local) or Streamlit secrets (cloud).")
    st.stop()

genai.configure(api_key=api_key)

try:
    MODEL_NAME = st.secrets["GOOGLE_MODEL"]
except:
    MODEL_NAME = os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")

# -------------------------------
# DATABASE SETUP
# -------------------------------
def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_name TEXT,
            role TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_message(chat_name, role, message):
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO chats (chat_name, role, message) VALUES (?, ?, ?)",
        (chat_name, role, message)
    )

    conn.commit()
    conn.close()


def load_chats():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("SELECT chat_name, role, message FROM chats")
    rows = c.fetchall()

    conn.close()

    chats = {}
    for chat_name, role, message in rows:
        if chat_name not in chats:
            chats[chat_name] = []
        chats[chat_name].append((role, message))

    return chats


init_db()

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
# SESSION STATE
# -------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

if "current_chat" not in st.session_state:
    if st.session_state.chats:
        st.session_state.current_chat = list(st.session_state.chats.keys())[0]
    else:
        st.session_state.current_chat = "Chat 1"
        st.session_state.chats["Chat 1"] = []

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("💬 Chats")

if st.sidebar.button("➕ New Chat"):
    new_chat = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat] = []
    st.session_state.current_chat = new_chat

st.sidebar.markdown("---")

for chat_name in st.session_state.chats.keys():
    if chat_name == st.session_state.current_chat:
        st.sidebar.markdown(f"👉 **{chat_name}**")
    else:
        if st.sidebar.button(chat_name):
            st.session_state.current_chat = chat_name

# -------------------------------
# MAIN UI
# -------------------------------
st.title("💬 AI Assistant")

# -------------------------------
# FUNCTION: GET RESPONSE
# -------------------------------
def get_response():
    try:
        conversation = SYSTEM_PROMPT + "\n\n"

        current_chat = st.session_state.chats[st.session_state.current_chat]
        recent_history = current_chat[-MAX_HISTORY:]

        for role, msg in recent_history:
            if role == "user":
                conversation += f"User: {msg}\n"
            else:
                conversation += f"Assistant: {msg}\n"

        model = genai.GenerativeModel(MODEL_NAME)

        response = model.generate_content(conversation)

        if not response or not response.text:
            return "⚠️ Empty response from AI."

        return response.text

    except Exception as e:
        print("ERROR:", str(e))
        return "❌ Something went wrong. Please try again."

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
    if len(user_input.strip()) == 0:
        st.warning("⚠️ Please enter a message")
    else:
        current_chat.append(("user", user_input))
        save_message(st.session_state.current_chat, "user", user_input)

        with st.spinner("Thinking... 🤖"):
            bot_response = get_response()

        current_chat.append(("assistant", bot_response))
        save_message(st.session_state.current_chat, "assistant", bot_response)

        st.rerun()
