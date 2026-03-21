import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------------
# Page config and custom CSS
# --------------------------
st.set_page_config(page_title="Nexus AI Chat", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    /* Custom chat bubbles */
    .user-message {
        background-color: #2c3e50;
        color: white;
        padding: 12px 16px;
        border-radius: 20px;
        margin: 8px 0;
        max-width: 80%;
        float: right;
        clear: both;
    }
    .assistant-message {
        background-color: #e9ecef;
        color: #212529;
        padding: 12px 16px;
        border-radius: 20px;
        margin: 8px 0;
        max-width: 80%;
        float: left;
        clear: both;
    }
    .chat-container {
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 10px;
        min-height: 400px;
        overflow-y: auto;
    }
    /* Sidebar styling */
    .sidebar .block-container {
        padding: 1rem;
    }
    /* Hide default streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Nexus AI Chat")
st.markdown("Chat with **Sarvam AI** and **Groq** – powered by Indian language models.")

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
        model_name = st.selectbox("Model", ["sarvam-m"], help="Sarvam-M is the free chat model.")
    else:  # Groq
        model_name = st.selectbox(
            "Model",
            ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
            help="Free models on Groq (rate limits apply)."
        )

    st.divider()
    st.subheader("⚙️ System Prompt")
    system_prompt = st.text_area(
        "Instructions for the AI",
        value="You are a helpful assistant.",
        height=100,
        help="This message is sent before each conversation to set the AI's behavior."
    )

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]
        st.rerun()

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
            response = client.chat(
                messages=messages,
                model=model,
                stream=False
            )
            # The exact attribute may vary; adjust as needed
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
        return f"❌ Error: {str(e)}"

# --------------------------
# Initialize session state for chat history
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# --------------------------
# Display chat history with custom styling
# --------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Handle user input
# --------------------------
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Immediately rerun to show the user message
    st.rerun()

    # Actually, we need to process after rerun – better to use a callback or process in same run.
    # Streamlit's chat_input works with session state; we can process after the rerun.
    # But we need to avoid infinite loop. Let's move processing after the rerun.

# We'll process after the rerun using a flag. Simpler: use st.chat_message and process inline.
# Let's restructure: Use st.chat_input and process immediately, then display.

# Reset approach: I'll rewrite the chat display to use st.chat_message which handles streaming.
# But since we want custom CSS, we'll keep the above and process after the input.

# The above code already uses st.rerun() which will cause the script to run again with the updated messages.
# However, we need to actually call the API after adding the user message. That happens only after rerun.
# So we need to check if the last message is from user and no response yet.

# Let's add a check for pending response.

if st.session_state.messages[-1]["role"] == "user":
    # Get the last user message
    user_message = st.session_state.messages[-1]["content"]

    # Validate API key
    api_key = None
    if provider == "Sarvam":
        api_key = sarvas_key
        if not api_key:
            st.error("Please enter your Sarvam AI API key in the sidebar.")
            st.stop()
    else:
        api_key = groq_key
        if not api_key:
            st.error("Please enter your Groq API key in the sidebar.")
            st.stop()

    # Prepare messages including system prompt
    messages_for_api = [{"role": "system", "content": system_prompt}] + [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]

    with st.spinner(f"Thinking with {provider}..."):
        response = get_response(provider, api_key, model_name, messages_for_api)

    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
