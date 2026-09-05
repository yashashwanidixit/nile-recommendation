from pathlib import Path
import pytest
from core.config import Settings, get_settings


def test_default_settings_initialization():
    settings = Settings()
    assert settings.HOST == "127.0.0.1"
    assert settings.PORT == 8000
    assert settings.ENVIRONMENT == "development"
    assert settings.DEBUG is False
    assert settings.PROJECT_NAME == "NILE Recommendation Engine"
    assert isinstance(settings.HOTELS_DATA_PATH, Path)
    assert isinstance(settings.ACTIVITIES_DATA_PATH, Path)
    assert "*" in settings.CORS_ORIGINS
    assert settings.LLM_API_KEY is None


def test_settings_environment_override(monkeypatch):
    monkeypatch.setenv("HOST", "0.0.0.0")
    monkeypatch.setenv("PORT", "9090")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LLM_MODEL", "gemini-1.5-pro")

    settings = Settings()
    assert settings.HOST == "0.0.0.0"
    assert settings.PORT == 9090
    assert settings.DEBUG is True
    assert settings.LLM_MODEL == "gemini-1.5-pro"


def test_get_settings_cache():
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2
