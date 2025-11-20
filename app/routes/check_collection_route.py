# General Imports
from fastapi import APIRouter
from qdrant_client import QdrantClient
from fastapi.responses import JSONResponse

# Package Imports
from app.core import app_config
from app.models import KnowledgeBaseInput

check_collection_router = APIRouter()

@check_collection_router.post("/check_collection")
def check_collection_exists(input: KnowledgeBaseInput)-> JSONResponse:
    """Check if the collection exists for the selected repo_name and repo_branch"""
    collection_name = f"{input.repo_name}-{input.repo_branch}".replace("/", "-").replace(".", "-")
    client = QdrantClient(url = app_config.qdrant_url)

    collections = client.get_collections().collections
    if collection_name in collections:
        return JSONResponse({"message": 1})
    else:
        return JSONResponse({"message": 0})