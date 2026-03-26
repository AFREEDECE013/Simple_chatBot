import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Gemini Chatbot")

st.title("💬 Gemini Chatbot")

# Configure API

genai.configure(api_key=api_key)

# Initialize model
# model = genai.GenerativeModel("gemini-pro")
model = genai.GenerativeModel("gemini-2.5-flash")

# Session state for chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get response
def get_gemini_response(query):
    response = st.session_state.chat.send_message(query, stream=True)
    
    full_response = ""
    for chunk in response:
        if chunk.text:
            full_response += chunk.text
    
    return full_response

# Input box
user_input = st.text_input("Type your message...")

if st.button("Send") and user_input:
    # Store user message
    st.session_state.chat_history.append(("You", user_input))
    
    # Get bot response
    bot_response = get_gemini_response(user_input)
    
    # Store bot response
    st.session_state.chat_history.append(("Bot", bot_response))

# Display chat history
st.subheader("Chat")

for role, text in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 {role}:** {text}")
    else:
        st.markdown(f"**🤖 {role}:** {text}")