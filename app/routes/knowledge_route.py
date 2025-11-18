# General Imports
from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Package Imports
from app.services import rag_pipeline
from app.models import KnowledgeBaseInput

knowledge_router = APIRouter()

@knowledge_router.post("/knowledge")
def build_knowledge_base(input: KnowledgeBaseInput)-> JSONResponse:
    """Knowledge base endpoint for building knowledge base"""
    rag_pipeline(input.repo_name,input.repo_branch)

    return JSONResponse({"message": "Successfully built knowledge base"})