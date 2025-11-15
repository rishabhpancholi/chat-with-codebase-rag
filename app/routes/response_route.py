# General Imports
from fastapi import APIRouter
from langchain_core.messages import HumanMessage

# Package Imports
from app.models import ChatInput
from app.services import chatbot

response_router = APIRouter()

@response_router.post("/respond")
def respond(input: ChatInput)->dict:
    """Response endpoint for user's query"""

    response = chatbot.invoke(
        {"messages":[HumanMessage(content = input.query)]},
        config = {"configurable": {"thread_id": input.thread_id}}
    )

    return {"response": response}

