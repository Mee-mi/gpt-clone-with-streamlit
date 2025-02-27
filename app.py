from groq import Groq
import streamlit as st
import os
from dotenv import load_dotenv


st.title("ChatGPT-like Clone with Groq API")


# Load environment variables
load_dotenv()
# Load API key manually if secrets fail
api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing. Check secrets.toml or set an environment variable.")
else:
    client = Groq(api_key=api_key)

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama-3.3-70b-versatile"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=st.session_state["groq_model"],
            messages=st.session_state.messages,
            stream=False,  # Set to True if you want to stream responses
        )
        assistant_message = response.choices[0].message.content 
        st.markdown(assistant_message)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})