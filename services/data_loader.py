from functools import lru_cache
import json
from pathlib import Path
from typing import Optional, Union

from core.config import get_settings
from core.exceptions import DataLoadError
from schemas.activity import Activity
from schemas.hotel import Hotel

DEFAULT_HOTELS_FILE = get_settings().HOTELS_DATA_PATH
DEFAULT_ACTIVITIES_FILE = get_settings().ACTIVITIES_DATA_PATH


def load_hotels(file_path: Optional[Union[str, Path]] = None) -> list[Hotel]:
    """Load and validate hotel records from a JSON file.

    Args:
        file_path: Optional path to hotels JSON file. Defaults to configured path.

    Returns:
        List of validated Hotel instances.
    """
    path = Path(file_path) if file_path else DEFAULT_HOTELS_FILE
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as err:
        raise DataLoadError(f"Failed to load hotels data from '{path}': {err}") from err

    if isinstance(data, dict) and "hotels" in data:
        items = data["hotels"]
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError("Expected list or dict with 'hotels' key in hotels JSON")

    return [Hotel.model_validate(item) for item in items]


def load_activities(file_path: Optional[Union[str, Path]] = None) -> list[Activity]:
    """Load and validate activity records from a JSON file.

    Args:
        file_path: Optional path to activities JSON file. Defaults to configured path.

    Returns:
        List of validated Activity instances.
    """
    path = Path(file_path) if file_path else DEFAULT_ACTIVITIES_FILE
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as err:
        raise DataLoadError(f"Failed to load activities data from '{path}': {err}") from err

    if isinstance(data, dict) and "activities" in data:
        items = data["activities"]
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError("Expected list or dict with 'activities' key in activities JSON")

    return [Activity.model_validate(item) for item in items]


@lru_cache(maxsize=1)
def get_cached_hotels(file_path: Optional[str] = None) -> list[Hotel]:
    """Load and cache hotel records in memory to prevent repeated JSON parsing."""
    return load_hotels(file_path)


@lru_cache(maxsize=1)
def get_cached_activities(file_path: Optional[str] = None) -> list[Activity]:
    """Load and cache activity records in memory to prevent repeated JSON parsing."""
    return load_activities(file_path)

