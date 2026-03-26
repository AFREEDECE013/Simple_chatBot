import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

google_model = os.getenv("GOOGLE_MODEL")

st.title("💬 Gemini Chatbot")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get response
def get_response(prompt):
    response = client.models.generate_content(
        model=google_model,
        contents=prompt
    )
    return response.text

# Input
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.chat_history.append(("user", user_input))

    # Get response
    bot_response = get_response(user_input)

    # Save bot response
    st.session_state.chat_history.append(("assistant", bot_response))

# Display chat
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)