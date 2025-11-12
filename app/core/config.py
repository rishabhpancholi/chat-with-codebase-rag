# General Imports
from pydantic_settings import BaseSettings,SettingsConfigDict

class AppConfig(BaseSettings):
    """Application config"""
    google_api_key: str
    github_personal_access_token: str
    model_config = SettingsConfigDict(env_file=".env")

app_config = AppConfig()
