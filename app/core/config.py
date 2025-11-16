# General Imports
from pydantic_settings import BaseSettings,SettingsConfigDict

class AppConfig(BaseSettings):
    """Application config"""
    google_api_key: str
    groq_api_key: str
    github_personal_access_token: str
    postgres_password: str
    postgres_user: str
    postgres_db: str
    langsmith_tracing: str
    langsmith_endpoint: str
    langsmith_api_key: str
    langsmith_project: str
    model_config = SettingsConfigDict(env_file=".env")

app_config = AppConfig()
