from schemas.activity import Activity
from schemas.hotel import Hotel
from schemas.intent import UserIntent


def filter_hotels(hotels: list[Hotel], intent: UserIntent) -> list[Hotel]:
    """Apply hard constraints to hotel candidates.

    Filters hotels based on hard criteria such as destination, availability,
    guest capacity, and required amenities.

    Args:
        hotels: List of hotel candidates.
        intent: Structured user travel intent.

    Returns:
        List of hotels passing all hard constraints.
    """
    pass


def filter_activities(activities: list[Activity], intent: UserIntent) -> list[Activity]:
    """Apply hard constraints to activity candidates.

    Filters activities based on hard criteria such as destination, availability,
    and category match.

    Args:
        activities: List of activity candidates.
        intent: Structured user travel intent.

    Returns:
        List of activities passing all hard constraints.
    """
    pass
