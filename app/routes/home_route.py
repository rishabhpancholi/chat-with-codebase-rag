# General Imports
from fastapi import APIRouter
from fastapi.responses import JSONResponse

home_router = APIRouter()

@home_router.get("/")
def home()-> JSONResponse:
    """Home endpoint"""
    return JSONResponse({"message": "Hello"})

@home_router.get("/health")
def health()-> JSONResponse:
    """Health endpoint"""
    return JSONResponse({"message": "Healthy"})