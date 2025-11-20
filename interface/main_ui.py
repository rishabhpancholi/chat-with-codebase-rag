# General Imports
import streamlit as st

# Package Imports
import uuid
from chat_ui import chat_interface
from utils import new_chat,get_chat,delete_chat,build_knowledge_base,collection_exists


# st.set_page_config(layout = "wide")

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = [st.session_state["thread_id"]]
if "vector_stores" not in st.session_state:
    st.session_state["vector_stores"] = set()
if "current_vector_store" not in st.session_state:
    st.session_state["current_vector_store"] = ""

st.sidebar.title("Chat with your codebase RAG")

if st.sidebar.button("New chat", key = "new_chat"):
    new_chat()

st.sidebar.header("My conversations")
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


st.sidebar.header("My knowledge bases")
selected_vector_store = st.sidebar.radio("Select knowledge base", [vector_store for vector_store in st.session_state["vector_stores"]] , key = "resume_vector_store")
st.session_state["current_vector_store"] = selected_vector_store

st.sidebar.header("Build Knowledge Base")
repo_name = st.sidebar.text_input("Repo Name", key = "repo_name")
repo_branch = st.sidebar.text_input("Repo Branch", key = "repo_branch")
if st.sidebar.button("Build Knowledge Base", key = "build_knowledge_base"):
    with st.sidebar.status("Building knowledge base...") as status:
        if not collection_exists(repo_name,repo_branch):
            status.update(label = "Collection already exists", state = "complete")
        else: 
            response = build_knowledge_base(repo_name,repo_branch)
            if response["message"] == "Successfully built knowledge base":
                status.update(label = "Successfully built knowledge base", state = "complete")
            else:
                status.update(label = "Error building knowledge base", state = "error")
        st.session_state["vector_stores"].add(f"{repo_name}-{repo_branch}".replace("/","-").replace(".","-"))
        st.session_state["current_vector_store"] = f"{repo_name}-{repo_branch}".replace("/","-").replace(".","-")
        st.rerun()

chat_interface()



