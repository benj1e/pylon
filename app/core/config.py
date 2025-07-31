from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import os

load_dotenv()
class Settings(BaseSettings):
    """Configuration settings for the application."""

    ngrok_public_url: str = Field(alias="NGROK_PUBLIC_URL", default=os.getenv("NGROK_PUBLIC_URL", ''))
    openrouter_api_key: str = Field(alias="OPENROUTER_API_KEY", default=os.getenv("OPENROUTER_API_KEY", ''))

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()