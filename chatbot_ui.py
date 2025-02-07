import streamlit as st
import requests

# FastAPI Backend URL
API_URL = "https://ai-tutor-zque.onrender.com/chat"

# Streamlit App Title
st.title("📚 AI Education Chatbot")

# Initialize Session State
if "subject" not in st.session_state:
    st.session_state.subject = None  # To store the subject name
if "messages" not in st.session_state:
    st.session_state.messages = []  # To store the conversation history

# Set Subject
if st.session_state.subject is None:
    subject = st.text_input("Enter the subject name for your exam:")
    if subject:
        st.session_state.subject = subject
        st.success(f"Subject set to: {subject}")
else:
    st.write(f"**Subject:** {st.session_state.subject}")

# Display Conversation History
st.write("### Conversation:")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
question = st.chat_input("Ask your question about this subject:")

# Submit Query

if question:
    # Add user's question to the conversation
    # st.session_state.message.append(question)
    with st.chat_message("user"):
        st.write(question)

    st.session_state.messages.append({"role": "user", "content": question})

    # Send request to backend
    payload = {"subject": st.session_state.subject, "question": question}
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        # Get AI's response
        answer = response.json().get("response", "No response received.")
        # Add AI's response to the conversation
        # st.session_state.message.append(answer)
        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

    else:
        st.error("Failed to get response from the AI backend.")

