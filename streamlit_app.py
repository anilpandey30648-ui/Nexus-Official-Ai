import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables (for deployment secrets)
load_dotenv()

st.set_page_config(page_title="AI Chat - Sarvam & Groq", page_icon="🤖", layout="wide")
st.title("🤖 AI Chat: Sarvam + Groq")
st.markdown("Chat with **Sarvam AI** (free Indian language model) or **Groq** (fast open‑source models).")

# --------------------------
# Sidebar configuration
# --------------------------
with st.sidebar:
    st.header("🔑 API Keys")
    sarvas_key = st.text_input(
        "Sarvam AI API Key",
        type="password",
        value=os.getenv("SARVAM_API_KEY", ""),
        help="Get your key from dashboard.sarvam.ai"
    )
    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="Get your key from console.groq.com"
    )

    st.divider()
    st.subheader("🤖 Model Selection")
    provider = st.selectbox("Choose Provider", ["Sarvam", "Groq"])

    if provider == "Sarvam":
        model_name = st.selectbox(
            "Model",
            ["sarvam-m"],
            help="Sarvam-M is the free chat model."
        )
    else:  # Groq
        model_name = st.selectbox(
            "Model",
            ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
            help="Free models on Groq (rate limits apply)."
        )

    st.divider()
    st.caption("API keys are only stored in your browser session and never saved.")

# --------------------------
# Helper: get response from API
# --------------------------
def get_response(provider, api_key, model, messages):
    """Send messages to the chosen API and return the reply."""
    try:
        if provider == "Sarvam":
            from sarvamai import SarvamAI
            client = SarvamAI(api_key=api_key)
            # Sarvam's chat method expects messages in a specific format
            # We'll assume it works like OpenAI's chat completion
            # Adjust if needed based on actual SDK documentation
            response = client.chat(
                messages=messages,
                model=model,
                stream=False
            )
            # Assume response has a .choices[0].message.content attribute
            return response.choices[0].message.content

        elif provider == "Groq":
            from groq import Groq
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=False
            )
            return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {e}"

# --------------------------
# Session state for chat history
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# --------------------------
# Display chat history
# --------------------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --------------------------
# Handle user input
# --------------------------
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Validate API key for selected provider
    api_key = None
    if provider == "Sarvam":
        api_key = sarvas_key
        if not api_key:
            st.error("Please enter your Sarvam AI API key in the sidebar.")
            st.stop()
    else:  # Groq
        api_key = groq_key
        if not api_key:
            st.error("Please enter your Groq API key in the sidebar.")
            st.stop()

    # Prepare messages (convert to the format expected by the APIs)
    # Sarvam and Groq both accept OpenAI‑style message list
    api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    # Get response
    with st.spinner("Thinking..."):
        response = get_response(provider, api_key, model_name, api_messages)

    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
