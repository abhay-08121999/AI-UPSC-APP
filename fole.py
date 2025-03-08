import streamlit as st
from streamlit_option_menu import option_menu
import requests
import time

# Gemini API Key (Replace with your actual API key from Google AI Studio)
GEMINI_API_KEY = "AIzaSyA4VTIRDM5qcYY_1ASnSioiX3s8WR3i2RE"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=GEMINI_API_KEY"

# ---------------------- Main App UI ----------------------
st.title("UPSC Preparation Hub")

with st.sidebar:
    selected = option_menu(
        "Main Menu", ["AI Tutor", "Feedbacks", "Group Discussion", "Mock Tests"],
        icons=["robot", "chat-dots", "people", "file-earmark-text"],
        menu_icon="cast", default_index=0)

# Function to fetch AI-generated responses using Gemini API
def get_ai_response(query):
    try:
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [
                {"parts": [{"text": f"You are an expert UPSC mentor. {query}"}]}
            ]
        }

        response = requests.post(GEMINI_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response received.")
        else:
            return f"API Error: {response.status_code}, {response.text}"

    except Exception as e:
        return f"Error: {e}"

# -------------------- AI TUTOR (Gemini API Integration) --------------------
if selected == "AI Tutor":
    st.header("AI Tutor")
    st.write("Ask your doubts and get AI-generated responses!")

    query = st.text_area("Enter your question")

    if st.button("Ask AI"):
        if query.strip() == "":
            st.warning("Please enter a question before submitting.")
        else:
            with st.spinner("Generating response..."):
                ai_response = get_ai_response(query)
                st.success("AI Response:")
                st.write(ai_response)

# -------------------- FEEDBACK SYSTEM --------------------
elif selected == "Feedbacks":
    st.header("Feedback System")
    feedback = st.text_area("Give your feedback or suggest improvements")
    if st.button("Submit Feedback"):
        st.success("Feedback submitted successfully!")

# -------------------- GROUP DISCUSSION --------------------
elif selected == "Group Discussion":
    st.header("Group Discussion Forum")
    st.write("Engage in discussions with other UPSC aspirants.")
    discussion = st.text_area("Post a message")
    if st.button("Send"):
        if discussion.strip() != "":
            st.success("Message sent!")
        else:
            st.warning("Message cannot be empty!")

# -------------------- MOCK TESTS --------------------
elif selected == "Mock Tests":
    st.header("Mock Tests")
    st.write("Take UPSC mock tests and evaluate your performance.")
    st.button("Start Mock Test")

st.sidebar.markdown("[Logout](#)")
