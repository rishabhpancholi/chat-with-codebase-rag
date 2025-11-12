import requests
import streamlit as st

st.title("Chat with your Codebase - RAG")

st.write("A chatbot that answers questions based on your codebase.")

query = st.chat_input("Enter your query:", key="query")

if query:
    with st.chat_message(name = "user", width = "content"):
        st.text(query)
    with st.chat_message(name = "assistant", width = "content"):
        with st.spinner("Thinking... please wait ⏳"):
            def stream_response():
                response_stream = requests.post("http://127.0.0.1:8000/respond",json={"query": query},stream = True)
                for response_chunk in response_stream.iter_lines(chunk_size = None, decode_unicode = True):
                    if response_chunk:
                        yield response_chunk
            st.write_stream(stream_response)