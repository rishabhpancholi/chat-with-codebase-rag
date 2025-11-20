# General Imports
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

def register_exception_handlers(app: FastAPI)-> None:
    """Register exception handlers for the FastAPI app."""
    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exc: Exception)-> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code= 500)