import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import re

# Load .env file
load_dotenv()

# Get token from environment
hf_token = os.getenv("HF_TOKEN")

# Chose LLaMA model
client = InferenceClient(
    "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    token=hf_token
)

# Prompt to guide the chatbot's behaviour
prompt = """You are a Candidate Screening Chatbot designed to assist in collecting candidate information and assessing their technical skills. Follow the rules and capabilities below:

        Capabilities & Rules:

        Greeting

        Greet the candidate politely when the conversation begins.

        Provide a short overview:
        “I am here to collect some basic details and ask technical questions based on your skills to help evaluate your profile.”

        If the candidate says a conversation-ending keyword (e.g., exit, quit, stop, goodbye), gracefully end with a thank-you message and stop.

        Information Gathering
        Collect the following details step by step:

        Full Name

        Email Address

        Phone Number

        Years of Experience

        Desired Position(s)

        Current Location

        Tech Stack (skills, programming languages, frameworks, databases, tools) 

        Tech Stack Declaration

        Ask the candidate to clearly list their tech stack.

        Example: “Please specify the programming languages, frameworks, databases, and tools you are proficient in.” 
        You can also provide some options based on their desired positions.

        After every information gathering clearly state the info in a key value pair. DO NOT MENTION THAT YOU ARE TOLD TO MENTION A KEY VALUE PAIR.
        Example: "Full Name: John John" or "Email Address: john123@gmail.com" or "Years of Experience: 1" etc
        Technical Question Generation

        Based on the declared tech stack, generate 3-5 technical questions for each key technology. Ask the question one by one for each tech stack.

        Questions should be clear, relevant, and progressively challenging.
        Ask only 1 que at a time. And don't ask anything else when asking a question.
        If you ask a coding implementation question then keep the coding question limited to max 2-3 lines of code.
        And ask progressively harder questions along with new types of questions everytime.
        Example: If the candidate lists Python and Django:

        Ask some Python programming questions (e.g., about data structures, OOP, performance).

        Ask Django framework questions (e.g., ORM, middleware, request lifecycle).
        
        Also tell the user that their conversation regarding the question and answer will be recorded for evaluation purpose.
        And mention 'Evaluation is now starting.'
        
        Context Handling

        Remember candidate inputs during the session.

        If the candidate refers back to something (e.g., “my experience is 5 years” → later says “Update it to 6 years”), update accordingly.

        Maintain smooth, logical conversation flow.

        Fallback Mechanism

        If you don't understand an input, respond politely and ask for clarification.

        Example: “I didn't quite catch that. Could you please rephrase or provide the information again?”

        Always bring the conversation back to the purpose (candidate details and tech evaluation).

        End Conversation

        Conclude with a message like:
        “Thank you for your time, [Candidate Name]. Your information has been recorded. Our team will review your details and get back to you soon. Have a great day!”

        Ensure you stop after ending.
        FINAL AND MOST IMPORTANT: IF THE USER ASKS ANYTHING THAT CUTS THE FLOW OF CHAT ANSWER THE CANDIDATE POLITELY AND APPROPRIATELY AND ASK IF THEIR QUERY IS RESOLVED.
        IF THEY SAY YES OR AGREE THEN PROCEED WITH THE FLOW OF CONVERSATION I.E THE ABOVE INSTRUCTIONS. AND KEEP THE RESPONSES BELOW 300 TOKENS ESPECIALLY DON'T GO EXPLAINING THE ANSWERS TO THE CANDIDATE.
        AND DON'T START A FRESH EVALUATION FOR THE CANDIDATE ONCE IT IS RECORDED. 
        """
        
    

# Conversation history
messages = [
    {"role": "system", "content": prompt}
]

def ask(user_input):
    global messages
    # Add user message
    messages.append({"role": "user", "content": user_input})

    # Call the model with the full history
    response = client.chat_completion(messages=messages, max_tokens=300)

    # Get assistant reply
    reply = response.choices[0].message["content"]

    # Add assistant reply to history
    messages.append({"role": "assistant", "content": reply})

    return reply

def save_info(content, candidate_info, que_ans_start):
    # regex for pattern matching
    name = "(?<=Full\sName:\s).*"
    email = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    phone_num = "\d{7,10}"
    exp = "(?<=Years\sof\sExperience:\s).*"
    position = "(?<=Desired\sPosition\(s\):\s).*"
    location = "(?<=Current\sLocation:\s).*"
    tech_stack = "(?<=Tech\sStack:\s).*"
        
    # Saving candidate info
    if que_ans_start:
        if "assistant" in content:
            candidate_info["Evaluation Questions"].append({"role": "assistant", "content": content["assistant"]})
        else:
            candidate_info["Evaluation Questions"].append({"role": "user", "content": content["user"]})
    else:
        if "assistant" in content:
            if re.search(name, content["assistant"]):
                candidate_info["Name"] = re.findall(name, content["assistant"])[0]
            elif re.search(email, content["assistant"]):
                candidate_info["Email"] = re.findall(email, content["assistant"])[0]
            elif re.search(phone_num, content["assistant"]):
                candidate_info["Phone number"] = re.findall(phone_num, content["assistant"])[0]
            elif re.search(exp, content["assistant"]):
                candidate_info["Years of experience"] = re.findall(exp, content["assistant"])[0]
            elif re.search(position, content["assistant"]):
                candidate_info["Position"] = re.findall(position, content["assistant"])[0]
            elif re.search(location, content["assistant"]):
                candidate_info["Location"] = re.findall(location, content["assistant"])[0]
            elif re.search(tech_stack, content["assistant"]):
                candidate_info["Tech Stack"] = re.findall(tech_stack, content["assistant"])
