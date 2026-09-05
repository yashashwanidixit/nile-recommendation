from functools import lru_cache
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = BASE_DIR / "data"


class Settings(BaseSettings):
    """Central application settings managed via pydantic-settings."""

    # Server configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Application metadata
    PROJECT_NAME: str = "NILE Recommendation Engine"
    PROJECT_DESCRIPTION: str = "AI-powered travel recommendation and itinerary service"
    VERSION: str = "0.1.0"

    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]

    # Dataset file paths
    HOTELS_DATA_PATH: Path = DEFAULT_DATA_DIR / "hotels.json"
    ACTIVITIES_DATA_PATH: Path = DEFAULT_DATA_DIR / "activities.json"

    # LLM settings (reserved for future LLM integration phase)
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()
