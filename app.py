import streamlit as st
from google import genai
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()


# Get API key from environment
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")


# Create Gemini client
client = genai.Client(
    api_key=api_key
)


# Configure Streamlit page
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖"
)


# Display title
st.title("🤖 Gemini AI Chatbot")


# Create session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []


# Create session state for Gemini conversation
if "previous_interaction_id" not in st.session_state:
    st.session_state.previous_interaction_id = None


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get user input
prompt = st.chat_input("Ask me anything...")


# Check if user entered something
if prompt:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # Display user message
    with st.chat_message("user"):
        st.write(prompt)


    # Display assistant response area
    with st.chat_message("assistant"):

        with st.spinner("Gemini is thinking..."):

            # First conversation
            if st.session_state.previous_interaction_id is None:

                interaction = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt
                )

            # Continue existing conversation
            else:

                interaction = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt,
                    previous_interaction_id=
                    st.session_state.previous_interaction_id
                )


            # Get AI response
            response = interaction.output_text


            # Display response
            st.write(response)


            # Save interaction ID
            st.session_state.previous_interaction_id = interaction.id


            # Save assistant message
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )
