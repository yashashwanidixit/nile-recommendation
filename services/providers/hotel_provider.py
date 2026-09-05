from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

from schemas.hotel import Hotel
from services.data_loader import load_hotels


class BaseHotelProvider(ABC):
    """Abstract interface for hotel data providers."""

    @abstractmethod
    def get_hotels(self) -> list[Hotel]:
        """Retrieve candidate hotels."""
        pass


class MockHotelProvider(BaseHotelProvider):
    """Mock hotel provider that loads hotels from JSON via data_loader."""

    def __init__(self, file_path: Optional[Union[str, Path]] = None) -> None:
        self.file_path = file_path

    def get_hotels(self) -> list[Hotel]:
        """Load and return hotels using existing data loader."""
        return load_hotels(self.file_path)


# Active provider instance (defaulting to MockHotelProvider)
_default_hotel_provider: BaseHotelProvider = MockHotelProvider()


def get_hotel_provider() -> BaseHotelProvider:
    """Get the currently configured hotel provider."""
    return _default_hotel_provider


def set_hotel_provider(provider: BaseHotelProvider) -> None:
    """Set the active hotel provider (enables swapping for future datasets or tests)."""
    global _default_hotel_provider
    _default_hotel_provider = provider


def get_hotels() -> list[Hotel]:
    """Retrieve hotels from the active provider."""
    return get_hotel_provider().get_hotels()
