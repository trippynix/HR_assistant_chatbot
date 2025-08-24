import streamlit as st
import re
from chatbot import ask, messages, save_info

# Candidate data storage
candidate_data = {"Evaluation Questions": []}

# Pattern to detect evaluation start
que_ans_flag_pattern = "Evaluation is now starting."

# Initialize session state for chat and flags
if "greeted" not in st.session_state:
    st.session_state.greeted = False
if "que_ans_start" not in st.session_state:
    st.session_state.que_ans_start = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {"Evaluation Questions": []}

st.title("💬 AI Interview Chatbot")

# 🔹 Trigger first greeting once at app start
if not st.session_state.greeted:
    reply = ask("")  # first greeting from bot
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.session_state.greeted = True

# Display chat messages
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**Assistant:** {chat['content']}")

# Chat input box
user_input = st.chat_input("Type your message...")

if user_input:
    print(st.session_state.candidate_data)
    # Save user input
    save_info({"user": user_input}, st.session_state.candidate_data, st.session_state.que_ans_start)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Get assistant reply
    reply = ask(user_input)

    # Check if evaluation started
    if re.search(que_ans_flag_pattern, reply):
        st.session_state.que_ans_start = True

    save_info({"assistant": reply}, st.session_state.candidate_data, st.session_state.que_ans_start)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    st.rerun()

