import streamlit as st
import re, uuid
from DB import insert_data
from chatbot import ask, save_info, prompt

# Pattern to detect evaluation start
que_ans_flag_pattern = "Evaluation is now starting."
end_patterns = ["exit", "quit", "stop", "goodbye"]

# Assign unique session_id
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
st.sidebar.write(f"Session ID: {st.session_state.session_id}")

# Initialize user-specific state
if "user_sessions" not in st.session_state:
    st.session_state.user_sessions = {}

if st.session_state.session_id not in st.session_state.user_sessions:
    st.session_state.user_sessions[st.session_state.session_id] = {
        "greeted": False,
        "que_ans_start": False,
        "chat_history": [],
        "candidate_data": {"Evaluation Questions": []},
        "conversation_ended": False,
        "messages": [ {"role": "system", "content": prompt} ]  # 👈 isolate history per user
    }

user_state = st.session_state.user_sessions[st.session_state.session_id]

st.title("💬 AI Interview Chatbot")

# Display chat messages
for chat in user_state["chat_history"]:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Greeting
if not user_state["greeted"]:
    reply = ask("", user_state["messages"])
    user_state["chat_history"].append({"role": "assistant", "content": reply})
    user_state["greeted"] = True
    st.rerun()

# Chat input
if user_input := st.chat_input("Type your message..."):
    save_info({"user": user_input}, user_state["candidate_data"], user_state["que_ans_start"])
    user_state["chat_history"].append({"role": "user", "content": user_input})

    reply = ask(user_input, user_state["messages"])   # 👈 pass per-user messages

    if re.search(que_ans_flag_pattern, reply):
        user_state["que_ans_start"] = True

    save_info({"assistant": reply}, user_state["candidate_data"], user_state["que_ans_start"])
    user_state["chat_history"].append({"role": "assistant", "content": reply})

    if any(word in user_input.lower() for word in end_patterns) or any(
        word in reply.lower() for word in ["thanks", "thank", "thankyou"]
    ):
        insert_data(user_state["candidate_data"])
        user_state["conversation_ended"] = True
        st.success("✅ Candidate data saved successfully!")

    st.rerun()
