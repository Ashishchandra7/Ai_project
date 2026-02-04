import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.caption("Ask anything about company policies 📄")

st.title("🤖 company policy Chatbot")

with st.sidebar:
    st.header("About")
    st.write("This chatbot answers company policy questions using RAG.")
    uploaded_file = st.file_uploader("Upload Company PDF", type="pdf")

if uploaded_file:
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("PDF Uploaded Successfully")


if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

    

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input box (ChatGPT style)
user_input = st.chat_input("Ask your question...")

if user_input:

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Call backend API
    response = requests.get(
        "http://127.0.0.1:8000/chat",
        params={"query": user_input}
    )

    answer = response.json()["answer"]

    # Show AI message
    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
