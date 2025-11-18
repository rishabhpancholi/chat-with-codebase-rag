# General Imports
import time
import requests
import streamlit as st

def chat_interface():
    """Chat interface for the app"""
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.text(message["content"])

    query = st.chat_input("Enter your message")

    if query:
        with st.chat_message(name = "user"):
            st.session_state["messages"].append({"role": "user", "content": query})
            st.text(query)
        with st.spinner("Generating response..."):
            with st.chat_message(name = "assistant"):
                response = requests.post("http://127.0.0.1:8000/respond", json = {"query": query, "thread_id": st.session_state["thread_id"], "vector_store": st.session_state["current_vector_store"]}).json()["response"]
                response_chunks = response["messages"][-1]["content"].split(" ")
                def response_event():
                    for response_chunk in response_chunks:
                        yield response_chunk + " "
                        time.sleep(0.05)
                st.write_stream(response_event)
            st.session_state["messages"].append({"role": "assistant", "content": response["messages"][-1]["content"]})