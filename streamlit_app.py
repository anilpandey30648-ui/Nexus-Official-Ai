 import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------------
# Page config
# --------------------------
st.set_page_config(
    page_title="Nexus AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# Custom CSS - Premium Dark Mode
# --------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }

    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        color: #cbd5e1;
        font-size: 1rem;
    }

    .model-badge {
        display: inline-block;
        padding: 6px 14px;
        background: rgba(102, 126, 234, 0.2);
        border-radius: 30px;
        font-size: 0.85rem;
        color: #a78bfa;
        margin-bottom: 1rem;
        text-align: center;
        width: 100%;
    }

    /* Sidebar */
    .sidebar .block-container {
        background: rgba(15, 23, 42, 0.95);
        border-radius: 20px;
        padding: 1rem;
    }

    /* Error message */
    .error-message {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        color: #ef4444;
        padding: 12px;
        border-radius: 12px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------
# Session state
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "typing" not in st.session_state:
    st.session_state.typing = False

# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    st.markdown("## ✨ Settings")

    sarvas_key = st.text_input(
        "Sarvam AI Key",
        type="password",
        value=os.getenv("SARVAM_API_KEY", ""),
        help="dashboard.sarvam.ai"
    )
    groq_key = st.text_input(
        "Groq Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="console.groq.com"
    )

    st.divider()
    provider = st.selectbox("Provider", ["Sarvam", "Groq"])

    if provider == "Sarvam":
        model_name = st.selectbox("Model", ["sarvam-m"])
    else:
        model_name = st.selectbox("Model", ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"])

    st.divider()
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful assistant.",
        height=100
    )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("🔒 Keys stay in your browser")

# --------------------------
# Main UI
# --------------------------
st.markdown("""
<div class="main-header">
    <h1>✨ Nexus AI</h1>
    <p>Intelligent conversations powered by Sarvam & Groq</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="model-badge">🔮 Active: {provider} • {model_name}</div>', unsafe_allow_html=True)

# --------------------------
# Chat display
# --------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.typing:
    with st.chat_message("assistant"):
        st.markdown("...")

# --------------------------
# Chat input & response
# --------------------------
prompt = st.chat_input("Type your message...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.typing = True
    st.rerun()

if st.session_state.typing and st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Get API key
    if provider == "Sarvam":
        api_key = sarvas_key
        if not api_key:
            st.markdown('<div class="error-message">⚠️ Please enter your Sarvam AI API key in the sidebar.</div>', unsafe_allow_html=True)
            st.session_state.typing = False
            st.stop()
    else:
        api_key = groq_key
        if not api_key:
            st.markdown('<div class="error-message">⚠️ Please enter your Groq API key in the sidebar.</div>', unsafe_allow_html=True)
            st.session_state.typing = False
            st.stop()

    # Prepare messages
    messages_for_api = [{"role": "system", "content": system_prompt}] + st.session_state.messages

    # Get response
    try:
        if provider == "Sarvam":
            from sarvamai import SarvamAI
            client = SarvamAI(api_key=api_key)
            response = client.chat(messages=messages_for_api, model=model_name, stream=False)
            reply = response.choices[0].message.content
        else:  # Groq
            from groq import Groq
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(model=model_name, messages=messages_for_api, stream=False)
            reply = response.choices[0].message.content
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.typing = False
    st.rerun()
