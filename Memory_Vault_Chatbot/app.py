import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import random
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="AI Multiverse - The Memory Vault",
    page_icon="🌌",
    layout="wide"
)

st.markdown("""
<style>
.main { background: #0E1117; }
</style>
""", unsafe_allow_html=True)

# Personalities and Prompt Modifiers
personalities = {
    "🦾 Iron Man": "You are Tony Stark (Iron Man). Speak confidently with humor and intelligence.",
    "🦇 Batman": "You are Batman. Be dark, serious and mysterious.",
    "🕵 Sherlock Holmes": "You are Sherlock Holmes. Answer with logical deductions.",
    "⚽ Ronaldo Fan": "You are Cristiano Ronaldo's biggest fan.",
    "💻 Hacker": "You are an ethical hacker who explains cybersecurity.",
    "🧙 Harry Potter": "You are Harry Potter from Hogwarts.",
    "🤣 Stand-up Comedian": "Always answer with jokes.",
    "🇺🇸 Donald Trump": "Talk like Donald Trump.",
    "🤖 Robot": "You are a futuristic AI robot.",
    "🧠 Albert Einstein": "Explain everything scientifically.",
    "⚡ Thor": "You are Thor, God of Thunder.",
    "😈 Loki": "You are Loki, clever and mischievous.",
    "🏏 Virat Kohli": "Speak like Virat Kohli.",
    "🚀 Elon Musk": "Talk like Elon Musk.",
    "📱 Steve Jobs": "Talk like Steve Jobs.",
    "🎬 Deadpool": "Talk like Deadpool with funny sarcasm."
}

styles = {
    "Friendly": "Be friendly.",
    "Funny": "Be humorous.",
    "Professional": "Be professional.",
    "Motivational": "Motivate the user.",
    "Short": "Keep replies concise."
}

lengths = {
    "Short": "Maximum 60 words.",
    "Medium": "Around 120 words.",
    "Long": "Around 250 words."
}

# SIDEBAR CONTROLS
st.sidebar.title("⚙️ Settings")

personality = st.sidebar.selectbox("Choose Personality", list(personalities.keys()))
reply_style = st.sidebar.selectbox("Response Style", list(styles.keys()))
reply_length = st.sidebar.selectbox("Response Length", list(lengths.keys()))

st.sidebar.divider()
if st.sidebar.button("🗑 CLEAR CHAT"):
    st.session_state.messages = []
    st.rerun()

st.title("🌌 THE MULTIVERSE OF CHATBOTS")
st.write("Talk to famous personalities from across the multiverse!")
st.info(f"Currently talking to **{personality}**")

# TASK 1: Initialize the Memory Vault
if "messages" not in st.session_state:
    st.session_state.messages = []

# TASK 2: Render the Chat History
for message in st.session_state.messages:
    # Adding avatars based on role to make it more appealing
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# TASK 3: Upgrade the Input UI
if user_message := st.chat_input("Say something..."):

    if len(user_message) > 500:
        st.error("Message should be less than 500 characters.")
        st.stop()
        
    # Render user message on screen immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_message)

    # TASK 4: Save User Message to Memory
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Prepare system prompt for Gemini
    system_prompt = f"{personalities[personality]}\n{styles[reply_style]}\n{lengths[reply_length]}\nStay completely in character."
    
    # Optional: We could pass the entire history to the AI to truly make it stateful for the LLM context.
    # For a simple implementation matching the prompt structure, we format the recent context.
    conversation_context = "\n".join(
        f"{'User' if m['role']=='user' else personality}: {m['content']}" 
        for m in st.session_state.messages[-5:] # Last 5 messages for context limit
    )
    
    full_prompt = f"{system_prompt}\n\nConversation Context:\n{conversation_context}"

    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🧠 AI is thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt
                )
                
                reply = response.text
                st.markdown(reply)
                
                # TASK 4: Save AI Message to Memory
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                st.error(f"Error communicating with AI: {e}")

st.divider()
st.subheader("📊 Chat Statistics")
total_messages = len(st.session_state.messages)
total_words = sum(len(msg["content"].split()) for msg in st.session_state.messages)

c1, c2 = st.columns(2)
c1.metric("Messages Exchanged", total_messages)
c2.metric("Total Words", total_words)

st.markdown("""
<div style='text-align:center; padding-top:20px; color:gray;'>
<hr>
🚀 <b>AI Multiverse v2.0 - Memory Vault Edition</b><br>
Developed using ❤️ Streamlit + Google Gemini
</div>
""", unsafe_allow_html=True)
