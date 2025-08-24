import streamlit as st
import re
from DB import insert_data
from chatbot import ask, save_info

# Pattern to detect evaluation start
que_ans_flag_pattern = "Evaluation is now starting."

# Pattern to detect conversation end
end_patterns = ["exit", "quit", "stop", "goodbye"]

# Initialize session state for chat and flags
if "greeted" not in st.session_state:
    st.session_state.greeted = False
if "que_ans_start" not in st.session_state:
    st.session_state.que_ans_start = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {"Evaluation Questions": []}
if "conversation_ended" not in st.session_state:
    st.session_state.conversation_ended = False

st.title("💬 AI Interview Chatbot")

# Display chat messages in bubbles
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Handle first greeting
if not st.session_state.greeted:
    reply = ask("")
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.session_state.greeted = True
    st.rerun()

# Input box for user
if user_input := st.chat_input("Type your message..."):
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
    
    # Detect if user ended conversation
    if any(word in user_input.lower() for word in end_patterns) or any(word in reply.lower() for word in ["thanks, thank, thankyou"]):
        # Insert candidate data into DB
        insert_data(st.session_state.candidate_data)
        st.session_state.conversation_ended = True
        st.success("✅ Candidate data saved successfully!")
        
    st.rerun()
