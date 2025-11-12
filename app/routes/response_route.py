# General Imports
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

# Package Imports
from app.models import ChatInput
from app.services import get_response

response_router = APIRouter()

@response_router.post("/respond")
async def respond(input: ChatInput)->StreamingResponse:
    """Response endpoint for user's query"""
    async def response_event():   
        async for response_chunk in get_response(input.query):
            if response_chunk:
                yield response_chunk

    return StreamingResponse(response_event(), media_type = "text/plain")

