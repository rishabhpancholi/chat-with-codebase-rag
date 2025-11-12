# General Imports
from typing import AsyncGenerator
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Package Imports
from app.core import app_config
from app.models import ChatState

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = app_config.google_api_key,
    streaming = True
)

def chat_node(state: ChatState)-> ChatState:
    """Takes user query and send it to LLM and returns response"""
    messages = state["messages"]
    response = llm.invoke(messages[-1].content)
    return {"messages": [response]}

graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot = graph.compile()

async def get_response(query: str)-> AsyncGenerator[str,None]:
    """Returns a response to a given query"""
    for message_chunk,_ in chatbot.stream(
        {"messages": [HumanMessage(content = query)]},
        stream_mode = "messages"
    ):
        
        if message_chunk.content:
            yield message_chunk.content


