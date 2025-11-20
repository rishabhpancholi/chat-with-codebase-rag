# General Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Package Imports
from app.core import register_exception_handlers
from app.routes import home_router,response_router,history_router,knowledge_router,check_collection_router

app = FastAPI(title = "Chat with your codebase RAG", description = "A chatbot that answers questions based on your codebase.", version = "1.0.0")

routers = [
    home_router,
    response_router,
    history_router,
    knowledge_router,
    check_collection_router
]

for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

register_exception_handlers(app)