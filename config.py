from pydantic import BaseSettings, Field
from typing import List, Optional
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Settings(BaseSettings):
    API_KEY: str = os.getenv('OPENAI_API_KEY')
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = Field(
        ["*"],
        env="CORS_ORIGINS",
    )

    # Optionally use this if you have more complex configurations
    MODEL: Optional[str] = Field(
        "text-davinci-003",  # Default OpenAI model
        env="MODEL",  # Load from environment variable
    )

    class Config:
        env_file = ".env"  # Load from .env file if present
        env_file_encoding = 'utf-8'

settings = Settings()