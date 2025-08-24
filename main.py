import streamlit as st
import re
from DB import insert_data
from chatbot import ask, save_info

# Patterns
que_ans_flag_pattern = "Evaluation is now starting."
end_patterns = ["exit", "quit", "stop", "goodbye"]

# --- UNIQUE SESSION KEYS (isolated per user) ---
if "session" not in st.session_state:
    st.session_state.session = {
        "greeted": False,
        "que_ans_start": False,
        "chat_history": [],
        "candidate_data": {"Evaluation Questions": []},
        "conversation_ended": False,
    }

state = st.session_state.session  # shorthand

# --- UI ---
st.title("💬 AI Interview Chatbot")

# Display chat messages in bubbles
for chat in state["chat_history"]:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Handle first greeting
if not state["greeted"]:
    reply = ask("")
    state["chat_history"].append({"role": "assistant", "content": reply})
    state["greeted"] = True
    st.rerun()

# Input box for user
if user_input := st.chat_input("Type your message..."):
    # Save user input
    save_info({"user": user_input}, state["candidate_data"], state["que_ans_start"])
    state["chat_history"].append({"role": "user", "content": user_input})

    # Get assistant reply
    reply = ask(user_input)

    # Check if evaluation started
    if re.search(que_ans_flag_pattern, reply):
        state["que_ans_start"] = True

    save_info({"assistant": reply}, state["candidate_data"], state["que_ans_start"])
    state["chat_history"].append({"role": "assistant", "content": reply})

    # Detect if conversation ended
    if (
        any(word in user_input.lower() for word in end_patterns)
        or any(word in reply.lower() for word in ["thanks", "thank", "thankyou"])
    ):
        insert_data(state["candidate_data"])
        state["conversation_ended"] = True
        st.success("✅ Candidate data saved successfully!")

    st.rerun()
