# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .chat-header h1 {
        margin: 0;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .chat-header p {
        margin: 10px 0 0 0;
        font-size: 1.1em;
        opacity: 0.9;
    }
    
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    
    .sidebar-content {
        padding: 1rem;
    }
    
    .stButton > button {
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .chat-message {
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    
    .export-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .model-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Google Gemini API Key - Replace with your actual API key
GEMINI_API_KEY = "AIzaSyDY7hbsK8pVPSG-i08-eed21m5bmxYPzQU"

# Configure Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Initialize Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    gemini_configured = True
except Exception as e:
    st.error(f"Failed to configure Gemini: {str(e)}")
    gemini_configured = False
    model = None

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main chat interface
def main():
    # Header
    with st.container():
        st.markdown("""
        <div class="chat-header">
            <h1>🤖 AI Chat Assistant</h1>
            <p>Powered by Google Gemini 1.5 Flash</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Check if Gemini is configured
    if not gemini_configured:
        st.error("❌ Gemini API not configured. Please check your API key.")
        return
    
    # Chat container
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat messages
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Assistant:</strong><br>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # User input
    user_prompt = st.chat_input("Type your message here...")
    
    # Handle user message
    if user_prompt:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Display user message
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>
            {user_prompt}
        </div>
        """, unsafe_allow_html=True)
        
        # Generate AI response
        with st.spinner("🤔 Thinking..."):
            try:
                response = model.generate_content(user_prompt)
                ai_response = response.text
                
                # Display AI response
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Assistant:</strong><br>
                    {ai_response}
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Assistant:</strong><br>
                    {error_msg}
                </div>
                """, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        # Rerun to refresh the display
        st.rerun()
    
    # Sidebar with controls
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        st.header("🎛 Chat Controls")
        
        # Clear chat button
        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Export chat
        if st.session_state.messages:
            st.subheader("📥 Export Options")
            
            # Export as text
            chat_export = ""
            for msg in st.session_state.messages:
                role_emoji = "👤" if msg["role"] == "user" else "🤖"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                chat_export += f"[{timestamp}] {role_emoji} {msg['role'].capitalize()}: {msg['content']}\n\n"
            
            st.download_button(
                "📄 Export as Text",
                chat_export,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Export as JSON
            import json
            json_export = json.dumps(st.session_state.messages, indent=2)
            st.download_button(
                "📊 Export as JSON",
                json_export,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Chat statistics
        if st.session_state.messages:
            st.subheader("📊 Chat Statistics")
            user_messages = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
            assistant_messages = len([msg for msg in st.session_state.messages if msg["role"] == "assistant"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("User Messages", user_messages)
            with col2:
                st.metric("AI Responses", assistant_messages)
            
            st.metric("Total Messages", len(st.session_state.messages))
        
        st.markdown("---")
        
        # Model info
        st.markdown("""
        <div class="model-info">
            <h4>🤖 Model Info</h4>
            <p><strong>Gemini 1.5 Flash</strong></p>
            <ul style="margin: 0; padding-left: 1rem;">
                <li>Fast & efficient responses</li>
                <li>Advanced reasoning</li>
                <li>Real-time chat</li>
                <li>Multimodal capabilities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
