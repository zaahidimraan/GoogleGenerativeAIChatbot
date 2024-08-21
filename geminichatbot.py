import streamlit as st
import google.generativeai as models
import os
from dotenv import load_dotenv

# Try to load from .env
load_dotenv()
api_key_from_env = os.getenv('API_KEY')

# Check if .env provided a valid key
if api_key_from_env:
    API_KEY = api_key_from_env
    print("API key loaded from .env")
else:
    # Fall back to Streamlit secrets
    if st.secrets is not None and "API_KEY" in st.secrets:
        API_KEY = st.secrets["API_KEY"]
        print("API key loaded from Streamlit secrets")
    else:
        API_KEY = None  # Or raise an error, depending on your needs
        print("Error: API key not found in .env or Streamlit secrets")
# Set your Google Generative AI API Key
models.configure(api_key=API_KEY)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to generate response from Google Generative AI
def generate_response(prompt):
    model = models.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Streamlit app
st.title("Google Generative AI Chatbot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Your message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response 
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = generate_response(prompt)
        message_placeholder.markdown(full_response)
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})