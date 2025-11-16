# General Imports
import psycopg
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.postgres import PostgresSaver

# Package Imports
# from app.core import app_config
from app.core import app_config
from app.models import ChatState,chat_model

def chat_node(state: ChatState)-> ChatState:
    """Takes user query and send it to LLM and returns response"""
    messages = state["messages"]
    response = chat_model.invoke(messages)
    return {"messages": [AIMessage(content = response)]}

def create_graph()-> StateGraph:
    conn = psycopg.connect(f"postgresql://{app_config.postgres_user}:{app_config.postgres_password}@localhost/{app_config.postgres_db}", autocommit = True)
    checkpointer = PostgresSaver(conn = conn)
    checkpointer.setup()

    graph = StateGraph(ChatState)
    graph.add_node("chat_node",chat_node)
    graph.add_edge(START,"chat_node")
    graph.add_edge("chat_node",END)

    chatbot = graph.compile(checkpointer = checkpointer)
    return chatbot

chatbot = create_graph()