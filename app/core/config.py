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
    model_config = SettingsConfigDict(env_file=".env")

app_config = AppConfig()
