# General Imports
from pydantic import BaseModel
from typing import TypedDict,Annotated,Optional,Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ChatInput(BaseModel):
    """Chat Input"""
    query: str
    thread_id: str
    vector_store: Optional[str]


class ChatState(TypedDict):
    """Chat State"""
    messages: Annotated[list[BaseMessage], add_messages]
    vector_store: str
    decision: Literal["Yes","No"]

class KnowledgeBaseInput(BaseModel):
    """Knowledge base input"""
    repo_name: str
    repo_branch: str

class DeciderNodeResponse(BaseModel):
    """Decider Node Response"""
    decision: Literal["Yes","No"]