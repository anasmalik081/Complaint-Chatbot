import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from chatbot.bot_logic import ChatSession
from chatbot.knowledge_base import load_knowledge_base
from chatbot.rag_chain import create_rag_chain

# Page settings
st.set_page_config(page_title="🤖 Cyfuture Chatbot", layout="centered")
st.title("🤖 Cyfuture Complaint Chatbot")
st.markdown("Easily file and track complaints using AI assistance.")

# Initialize chatbot and RAG pipeline
if "chatbot" not in st.session_state:
    doc_path = "sample_docs/sample_faqs.pdf"
    vectorstore = load_knowledge_base(doc_path)
    rag_chain = create_rag_chain(vectorstore)

    st.session_state.chatbot = ChatSession()
    st.session_state.rag_chain = rag_chain
    st.session_state.chat_history = []

# Chat input box
user_input = st.chat_input("Type your message here...")

if user_input:
    bot = st.session_state.chatbot
    rag = st.session_state.rag_chain

    # Store user message
    st.session_state.chat_history.append(("user", user_input))

    # Get bot response
    response = bot.handle_input(user_input, rag)

    # Store bot message
    st.session_state.chat_history.append(("bot", response))

# Display chat messages
for sender, msg in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(msg)
