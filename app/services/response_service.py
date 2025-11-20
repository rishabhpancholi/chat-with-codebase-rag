# General Imports
import psycopg
from typing import Literal
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_qdrant import QdrantVectorStore
from langgraph.graph import StateGraph,START,END
from langchain_core.prompts import PromptTemplate
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.output_parsers import StrOutputParser

# Package Imports
# from app.core import app_config
from app.core import app_config
from app.models import ChatState,DeciderNodeResponse,llm,embeddings_model

load_dotenv()

def decider_node(state: ChatState)-> ChatState:
    """Decides next node to be executed based on user query or presence of vector store"""
    if state["vector_store"] == "":
        return {"decision": "No"}
    decider_llm  = llm.with_structured_output(DeciderNodeResponse)
    query = state["messages"][-1].content
    decider_node_prompt = PromptTemplate(
        input_variables = ["query"],
        template = """
        You are a decider node in a workflow. Your task is to decide which node to execute next based on the user's query.
        Return Yes if the query requires retrieval from a vector database related to a github repo or any code file and No if it does not. Here is the user's query: {query}
        """
    )
    decision = decider_llm.invoke(decider_node_prompt.format(query = query)).decision
    return {"decision": decision}

def deciding_condition(state: ChatState)-> Literal["chat_node_with_retrieval","chat_node"]:
    """Deciding condition for which chat node to go to"""
    if state["decision"] == "Yes":
        return "chat_node_with_retrieval"
    elif state["decision"] == "No":
        return "chat_node"

def chat_node(state: ChatState)-> ChatState:
    """Takes user query and send it to LLM and returns response"""
    messages = state["messages"]
    chat_model = llm | StrOutputParser()
    response = chat_model.invoke(messages)
    return {"messages": [AIMessage(content = response)]}

def chat_node_with_retrieval(state: ChatState)-> ChatState:
    """Takes user query and retrieves context from vector database and send it to LLM and returns response"""
    qdrant_vectorstore = QdrantVectorStore.from_existing_collection(
        url = "http://localhost:6333/",
        collection_name = state["vector_store"],
        embedding = embeddings_model
    )
    retriever = qdrant_vectorstore.as_retriever(search_kwargs = {"k":5})
    query = state["messages"][-1].content
    context_docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in context_docs])
    messages = state["messages"]
    conversation = ""
    for message in messages:
        if not isinstance(message,AIMessage):
            conversation += f"user's query: {message.content}\n\n"
        else:
            conversation += f"your reply: {message.content}\n\n"
          
    prompt = PromptTemplate(
        input_variables = ["query","context","conversation"],
        template = """
        You are a helpful assistant. The user has provided you the query: {query}.
        You also have a context string {context}. Read the context and provide an answer to the query strictly from the given context. And start your answer with the line 'Based on the available code...'
        If you dont know the answer just say i dont know. Dont make up an answer on your own. Here is the message history between you and the user for context as well:
        {conversation}
        """
    )
    chat_model = prompt | llm | StrOutputParser()
    response = chat_model.invoke({"query": query, "context": context, "conversation": conversation})
    return {"messages": [AIMessage(content = response)]}

def create_graph()-> StateGraph:
    conn = psycopg.connect(f"postgresql://{app_config.postgres_user}:{app_config.postgres_password}@localhost/{app_config.postgres_db}", autocommit = True)
    checkpointer = PostgresSaver(conn = conn)
    checkpointer.setup()

    graph = StateGraph(ChatState)
    graph.add_node("decider_node", decider_node)
    graph.add_node("chat_node_with_retrieval", chat_node_with_retrieval)
    graph.add_node("chat_node", chat_node)

    graph.add_edge(START,"decider_node")
    graph.add_conditional_edges("decider_node", deciding_condition)
    graph.add_edge("chat_node_with_retrieval",END)
    graph.add_edge("chat_node",END)

    chatbot = graph.compile(checkpointer = checkpointer)
    return chatbot

chatbot = create_graph()