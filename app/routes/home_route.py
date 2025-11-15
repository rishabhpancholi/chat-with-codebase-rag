# General Imports
from fastapi import APIRouter

home_router = APIRouter()

@home_router.get("/")
def home():
    """Home endpoint"""
    return {"message": "Hello"}

@home_router.get("/health")
def health():
    """Health endpoint"""
    return {"message": "Everything is fine"}