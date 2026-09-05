from schemas.activity import Activity
from schemas.hotel import Hotel
from schemas.intent import UserIntent


def is_hotel_eligible(hotel: Hotel, intent: UserIntent) -> bool:
    """Evaluate whether a single hotel satisfies all hard constraints.

    Constraint checks (in order):
    1. Destination match: hotel.destination == intent.destination
    2. General availability: hotel.availability is True
    3. Group capacity: hotel.max_guests >= intent.group_size
    4. Required preferences: Every required item in intent.preferences.required
       must exist in hotel.amenities or hotel.tags (AND semantics).

    Note:
    - Preferred preferences (intent.preferences.preferred) are soft and NOT filtered here.
    - Rating, partnered status, and budget are NOT hard-filtered at this stage.

    Args:
        hotel: Candidate Hotel domain model.
        intent: User travel intent.

    Returns:
        True if all hard constraints pass, False otherwise.
    """
    # Filter A: Destination match
    if hotel.destination != intent.destination:
        return False

    # Filter B: General availability
    if not hotel.availability:
        return False

    # Filter C: Group capacity
    if hotel.max_guests < intent.group_size:
        return False

    # Filter D: Required preferences (AND semantics across combined amenities + tags)
    if intent.preferences.required:
        hotel_features = set(hotel.amenities).union(hotel.tags)
        for req in intent.preferences.required:
            if req not in hotel_features:
                return False

    return True


def filter_hotels(hotels: list[Hotel], intent: UserIntent) -> list[Hotel]:
    """Apply deterministic hard constraints to hotel candidates.

    Args:
        hotels: Candidate hotels list.
        intent: Structured user travel intent.

    Returns:
        New list of eligible Hotel objects (original objects are unmutated).
    """
    return [hotel for hotel in hotels if is_hotel_eligible(hotel, intent)]


def is_activity_eligible(activity: Activity, intent: UserIntent) -> bool:
    """Evaluate whether a single activity satisfies all hard constraints.

    Constraint checks (in order):
    1. Destination match: activity.destination == intent.destination
    2. General availability: activity.availability is True
    3. Requested category: activity.category must be present in intent.activities
       (OR semantics across requested categories).

    Note:
    - Activity capacity (max_capacity) is NOT a hard filter.
    - Group type (suitable_for) is NOT a hard filter.
    - Price and opening/closing times are NOT hard filters at this stage.

    Args:
        activity: Candidate Activity domain model.
        intent: User travel intent.

    Returns:
        True if all hard constraints pass, False otherwise.
    """
    # Filter A: Destination match
    if activity.destination != intent.destination:
        return False

    # Filter B: General availability
    if not activity.availability:
        return False

    # Filter C: Requested activity category (OR semantics across requested categories)
    if activity.category not in intent.activities:
        return False

    return True


def filter_activities(activities: list[Activity], intent: UserIntent) -> list[Activity]:
    """Apply deterministic hard constraints to activity candidates.

    Args:
        activities: Candidate activities list.
        intent: Structured user travel intent.

    Returns:
        New list of eligible Activity objects (original objects are unmutated).
    """
    return [activity for activity in activities if is_activity_eligible(activity, intent)]
