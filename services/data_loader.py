import json
from pathlib import Path
from typing import Optional, Union

from schemas.activity import Activity
from schemas.hotel import Hotel

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_HOTELS_FILE = DATA_DIR / "hotels.json"
DEFAULT_ACTIVITIES_FILE = DATA_DIR / "activities.json"


def load_hotels(file_path: Optional[Union[str, Path]] = None) -> list[Hotel]:
    """Load and validate hotel records from a JSON file.

    Args:
        file_path: Optional path to hotels JSON file. Defaults to data/hotels.json.

    Returns:
        List of validated Hotel instances.
    """
    path = Path(file_path) if file_path else DEFAULT_HOTELS_FILE
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

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
        file_path: Optional path to activities JSON file. Defaults to data/activities.json.

    Returns:
        List of validated Activity instances.
    """
    path = Path(file_path) if file_path else DEFAULT_ACTIVITIES_FILE
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "activities" in data:
        items = data["activities"]
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError("Expected list or dict with 'activities' key in activities JSON")

    return [Activity.model_validate(item) for item in items]
