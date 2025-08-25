# Hiring Assistant Chatbot 🤖

## Project Overview
The **Hiring Assistant Chatbot** is an AI-powered system designed to streamline the hiring process.  
It interacts with candidates via a **Streamlit web interface**, gathers personal information, and asks technical questions.  
The chatbot stores candidate data in **MongoDB** for easy retrieval and analysis.

Key Features:
- Conversational interface for candidate screening.
- Stores candidate information in MongoDB.
- Asks both personal and technical questions.
- Session-state handling to manage multiple users.
- Built with **Streamlit**, **LangChain/Transformers**, and **PyTorch**.

---

## Installation Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/hiring-assistant-chatbot.git
cd hiring-assistant-chatbot
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate # On Mac/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the project root:
```bash
MONGO_URI=your_mongodb_connection_string
HF_TOKEN=your_huggingface_token  # if using HuggingFace models
```

### 5. Run the Application
```bash
streamlit run main.py
```

---

## Usage Guide

### 1. Open the Streamlit app in your browser (http://localhost:8501).
### 2. Start chatting with the Hiring Assistant.

### 3. Candidate data will be stored automatically in MongoDB.

### 4. Multiple users can interact simultaneously thanks to session state handling.

---

## Technical Details

- Frontend & Hosting: Streamlit

- Backend Logic: Python

- Database: MongoDB (via pymongo)

- LLM Support: Transformers (with PyTorch backend), HuggingFace

- State Management: Streamlit session state per user session

### Architecture:

- main.py → Streamlit web interface & session management

- chatbot.py → Chat logic, prompt design, candidate Q&A

- db.py → MongoDB connection & insert logic

---

## Prompt Design
The prompts were carefully designed to:

- Start with personal information gathering (name, email, role applied for).

- Transition into technical evaluation questions.

- Ensure context-awareness so the chatbot remembers candidate inputs.

- Use controlled formatting to store structured data in MongoDB.

---

## Challenges & Solutions

- *Challenge*: Handling multiple users in real-time.
  *Solution*: Implemented Streamlit session_state to isolate each conversation.

- *Challenge*: Large model dependencies causing memory errors.
  *Solution*: Used lightweight HuggingFace models.

- *Challenge*: Ensuring clean database writes.
  *Solution*: Centralized MongoDB insert logic in db.py.

---

## Requirements

See requirements.txt for full dependency list.

---

This setup ensures:

- The chatbot runs locally
- MongoDB is properly connected
