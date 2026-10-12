from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

from schemas.activity import Activity
from services.data_loader import get_cached_activities, load_activities


class BaseActivityProvider(ABC):
    """Abstract interface for activity data providers."""

    @abstractmethod
    def get_activities(self) -> list[Activity]:
        """Retrieve candidate activities."""
        pass


class MockActivityProvider(BaseActivityProvider):
    """Mock activity provider that loads activities from JSON via data_loader."""

    def __init__(self, file_path: Optional[Union[str, Path]] = None) -> None:
        self.file_path = file_path

    def get_activities(self) -> list[Activity]:
        """Load and return activities using cached data loader by default, or fresh load for custom paths."""
        if self.file_path:
            return load_activities(self.file_path)
        return get_cached_activities()


# Active provider instance (defaulting to MockActivityProvider)
_default_activity_provider: BaseActivityProvider = MockActivityProvider()


def get_activity_provider() -> BaseActivityProvider:
    """Get the currently configured activity provider."""
    return _default_activity_provider


def set_activity_provider(provider: BaseActivityProvider) -> None:
    """Set the active activity provider (enables swapping for future datasets or tests)."""
    global _default_activity_provider
    _default_activity_provider = provider


def get_activities() -> list[Activity]:
    """Retrieve activities from the active provider."""
    return get_activity_provider().get_activities()
