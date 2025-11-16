# General Imports
import streamlit as st

# Package Imports
import uuid
from chat_ui import chat_interface
from utils import new_chat,get_chat,delete_chat


st.set_page_config(layout = "wide")

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = [st.session_state["thread_id"]]

st.sidebar.title("Chat with your codebase RAG")

if st.sidebar.button("New chat", key = "new_chat"):
    new_chat()


if len(st.session_state["chat_threads"])==1:
    if st.sidebar.button("Resume Chat", key = f"resume_{st.session_state["thread_id"]}"):
        get_chat(st.session_state["thread_id"])
else:
    for idx,thread_id in enumerate(st.session_state["chat_threads"]):
            col1,col2 = st.sidebar.columns([3,1])

            with col1:
                if st.button("Resume Chat", key = f"resume_{thread_id}"):
                    get_chat(thread_id)
            with col2:
                if st.button("🗑️", key = f"delete_{thread_id}", help = "Delete this chat"):
                    delete_chat(thread_id)

chat_interface()

