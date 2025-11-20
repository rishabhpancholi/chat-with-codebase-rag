# General Imports
from fastapi import APIRouter
from langchain_core.messages import HumanMessage

# Package Imports
from app.models import ChatInput
from app.services import chatbot
from app.cache import get_cached_response, set_cached_response

response_router = APIRouter()

@response_router.post("/respond")
def respond(input: ChatInput)->dict:
    """Response endpoint for user's query"""

    cache_key = f"{input.query}-{input.thread_id}-{input.vector_store}"
    cached_response = get_cached_response(cache_key)

    if cached_response:
        return {"response": cached_response}

    response = chatbot.invoke(
        {"messages":[HumanMessage(content = input.query)], "vector_store": input.vector_store},
        config = {
            "configurable": {"thread_id": input.thread_id},
            "metadata": {"thread_id": input.thread_id, "vector_store": input.vector_store},
            "run_name": "chat_turn"
        }
    )
    set_cached_response(cache_key, response["messages"][-1].content)

    return {"response": response["messages"][-1].content}

