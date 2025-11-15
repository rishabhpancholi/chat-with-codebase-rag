# General Imports
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Package Imports
from app.core import app_config

chat_model = ChatGroq(
    model = "llama-3.1-8b-instant",
    groq_api_key = app_config.groq_api_key,
)

embeddings_model = GoogleGenerativeAIEmbeddings(
    model = "models/gemini-embedding-001",
    google_api_key = app_config.google_api_key,
)