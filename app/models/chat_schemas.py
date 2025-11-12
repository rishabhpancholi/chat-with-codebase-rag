# General Imports
from pydantic import BaseModel
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    """Chat State"""
    messages: Annotated[list[BaseMessage], add_messages]

class ChatInput(BaseModel):
    """Input for chatbot"""
    query: str