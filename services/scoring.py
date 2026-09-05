from schemas.activity import Activity
from schemas.hotel import Hotel
from schemas.intent import UserIntent


def score_hotels(
    hotels: list[Hotel], intent: UserIntent
) -> list[tuple[Hotel, float, list[str]]]:
    """Calculate recommendation scores for hotel candidates.

    Scores candidates using soft factors like preferred tags/amenities, rating,
    budget fit, and partnership status.

    Args:
        hotels: Candidate hotels that passed hard filtering.
        intent: Structured user travel intent.

    Returns:
        List of tuples containing (hotel, score, match_reasons).
    """
    pass


def score_activities(
    activities: list[Activity], intent: UserIntent
) -> list[tuple[Activity, float, list[str]]]:
    """Calculate recommendation scores for activity candidates.

    Scores candidates using soft factors like preferred tags, ratings,
    and suitability.

    Args:
        activities: Candidate activities that passed hard filtering.
        intent: Structured user travel intent.

    Returns:
        List of tuples containing (activity, score, match_reasons).
    """
    pass
