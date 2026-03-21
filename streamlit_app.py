import os
import streamlit as st
from dotenv import load_dotenv
import time

load_dotenv()

# --------------------------
# Page config
# --------------------------
st.set_page_config(
    page_title="Nexus AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------
# Custom CSS - Premium Dark Mode
# --------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Main container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .header h1 {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .header p {
        color: #cbd5e1;
        font-size: 1.1rem;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 20px;
        min-height: 60vh;
        max-height: 70vh;
        overflow-y: auto;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Scrollbar */
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 20px;
        margin: 12px 0;
        max-width: 70%;
        margin-left: auto;
        word-wrap: break-word;
        animation: slideInRight 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .assistant-message {
        background: rgba(51, 65, 85, 0.8);
        color: #e2e8f0;
        padding: 12px 20px;
        border-radius: 20px;
        margin: 12px 0;
        max-width: 70%;
        margin-right: auto;
        word-wrap: break-word;
        animation: slideInLeft 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 12px 20px;
        background: rgba(51, 65, 85, 0.8);
        border-radius: 20px;
        margin: 12px 0;
        width: fit-content;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #667eea;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.5;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1rem;
        margin: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Input field */
    .stChatInput > div > div {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 30px;
        color: white;
    }
    
    .stChatInput > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: #1e293b;
        border-color: #334155;
        color: white;
    }
    
    /* Text area */
    .stTextArea > div > div {
        background: #1e293b;
        border-color: #334155;
        color: white;
    }
    
    /* Labels */
    .stMarkdown label {
        color: #cbd5e1;
        font-weight: 500;
    }
    
    /* Model badge */
    .model-badge {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        font-size: 0.85rem;
        color: #a78bfa;
        margin-bottom: 1rem;
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
# Initialize session state
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "typing" not in st.session_state:
    st.session_state.typing = False
if "provider" not in st.session_state:
    st.session_state.provider = "Sarvam"
if "model_name" not in st.session_state:
    st.session_state.model_name = "sarvam-m"

# --------------------------
# Sidebar (hidden by default, appears on hover/click)
# --------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h3 style="color: white; margin-bottom: 1rem;">✨ Settings</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🔑 API Keys")
    sarvas_key = st.text_input(
        "Sarvam AI Key",
        type="password",
        value=os.getenv("SARVAM_API_KEY", ""),
        placeholder="Enter your key",
        help="Get from dashboard.sarvam.ai"
    )
    groq_key = st.text_input(
        "Groq Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        placeholder="Enter your key",
        help="Get from console.groq.com"
    )
    
    st.divider()
    
    st.subheader("🤖 Model")
    provider = st.selectbox(
        "Provider",
        ["Sarvam", "Groq"],
        index=0 if st.session_state.provider == "Sarvam" else 1
    )
    
    if provider == "Sarvam":
        model_name = st.selectbox("Model", ["sarvam-m"])
    else:
        model_name = st.selectbox("Model", ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"])
    
    st.divider()
    
    st.subheader("⚙️ System Prompt")
    system_prompt = st.text_area(
        "Instructions",
        value="You are a helpful assistant.",
        height=100,
        help="Sets the AI's behavior"
    )
    
    st.divider()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("🔒 Keys stay in your browser")

# Update session state
st.session_state.provider = provider
st.session_state.model_name = model_name

# --------------------------
# Main UI
# --------------------------
st.markdown("""
<div class="header">
    <h1>✨ Nexus AI</h1>
    <p>Intelligent conversations powered by Sarvam & Groq</p>
</div>
""", unsafe_allow_html=True)

# Model badge
st.markdown(f'<div class="model-badge">🔮 Active: {provider} • {model_name}</div>', unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

# Typing indicator
if st.session_state.typing:
    st.markdown("""
    <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Helper functions
# --------------------------
def get_response(provider, api_key, model, messages):
    try:
        if provider == "Sarvam":
            from sarvamai import SarvamAI
            client = SarvamAI(api_key=api_key)
            response = client.chat(messages=messages, model=model, stream=False)
            return response.choices[0].message.content
        elif provider == "Groq":
            from groq import Groq
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(model=model, messages=messages, stream=False)
            return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --------------------------
# Chat input
# --------------------------
prompt = st.chat_input("Type your message...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.typing = True
    st.rerun()

# Process response if last message is from user
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and st.session_state.typing:
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
    response = get_response(provider, api_key, model_name, messages_for_api)
    
    # Add response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.typing = False
    st.rerun()
