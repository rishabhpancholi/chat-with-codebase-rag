# General Imports
from fastapi import APIRouter

# Package Imports
from app.services import chatbot

history_router = APIRouter()

@history_router.get("/history")
def give_history(thread_id: str)-> dict:
    state = chatbot.get_state(
        config = {"configurable": {"thread_id": thread_id}}
    )

    return {"messages": [m for m in state.values["messages"]]}

