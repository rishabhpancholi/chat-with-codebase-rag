# General Imports
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers.string import StrOutputParser

# Package Imports
from app.core import app_config

load_dotenv()

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    groq_api_key = app_config.groq_api_key,
)

chat_model = llm | StrOutputParser()

embeddings_model = GoogleGenerativeAIEmbeddings(
    model = "models/gemini-embedding-001",
    google_api_key = app_config.google_api_key,
)