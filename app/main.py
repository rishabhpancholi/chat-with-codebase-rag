# General Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Package Imports
from app.routes import home_router,response_router,history_router

app = FastAPI(title = "Chat with your codebase RAG", description = "A chatbot that answers questions based on your codebase.", version = "1.0.0")

app.include_router(home_router)
app.include_router(response_router)
app.include_router(history_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)