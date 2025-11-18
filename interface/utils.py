# General Imports
import uuid
import requests
import streamlit as st

def new_chat()-> None:
    """Reset the chat session"""
    st.session_state["thread_id"] = str(uuid.uuid4())
    st.session_state["messages"] = []
    st.session_state["chat_threads"].append(st.session_state["thread_id"])

def get_chat(thread_id: str)-> None:
    """Get the chat history for the selected thread_id"""
    chat_messages = []
    try:
        response = requests.get(f"http://127.0.0.1:8000/history?thread_id={thread_id}").json()
    except Exception:
        response = {"messages": []}
    
    st.session_state["thread_id"] = thread_id
    st.session_state["messages"] = []
    chat_messages = response["messages"]
    for message in chat_messages:
        if message["type"] == "human":
            st.session_state["messages"].append({"role": "user", "content": message["content"]})
        elif message["type"] == "ai":
            st.session_state["messages"].append({"role": "assistant", "content": message["content"]})

def delete_chat(thread_id: str)-> None:
    """Delete the chat history for the selected thread_id"""
    st.session_state["messages"] = []
    st.session_state["chat_threads"].remove(thread_id)
    st.rerun()

# def build_knowledge_base(repo_name: str,repo_branch: str)-> dict:
#     """Build the knowledge base for the selected repo_name and repo_branch"""
#     response = requests.post("http://127.0.0.1:8000/knowledge", json = {"repo_name": repo_name, "repo_branch": repo_branch}).json()
#     return response
    
        
