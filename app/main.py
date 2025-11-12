# General Imports
from fastapi import FastAPI

# Package Imports
from app.routes import response_router

app = FastAPI(title = "Chat with your codebase RAG", description = "A chatbot that answers questions based on your codebase.", version = "1.0.0")

app.include_router(response_router)