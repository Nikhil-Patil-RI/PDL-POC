"""
Configuration settings for PDL-POC.
"""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # PDL API Configuration
    pdl_api_key: str = os.getenv("PDL_KEY", "")

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Prospect Generation Settings
    default_page_size: int = 25
    max_page_size: int = 100
    max_preview_prospects: int = 100
    min_preview_prospects: int = 10

    # Export Settings
    export_directory: str = "exports"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()

