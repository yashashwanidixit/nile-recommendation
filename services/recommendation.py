from schemas.activity import Activity
from schemas.hotel import Hotel
from schemas.intent import UserIntent
from schemas.recommendation import RecommendationItem, RecommendationOutput


def recommend_hotels(
    hotels: list[Hotel], intent: UserIntent, top_k: int = 5
) -> list[RecommendationItem]:
    """Return ranked hotel recommendations.

    Args:
        hotels: Candidate hotels list.
        intent: Structured user travel intent.
        top_k: Number of top recommendations to return.

    Returns:
        List of ranked RecommendationItem objects for hotels.
    """
    pass


def recommend_activities(
    activities: list[Activity], intent: UserIntent, top_k: int = 5
) -> list[RecommendationItem]:
    """Return ranked activity recommendations.

    Args:
        activities: Candidate activities list.
        intent: Structured user travel intent.
        top_k: Number of top recommendations to return.

    Returns:
        List of ranked RecommendationItem objects for activities.
    """
    pass


def get_recommendations(
    hotels: list[Hotel], activities: list[Activity], intent: UserIntent
) -> RecommendationOutput:
    """Orchestrate end-to-end recommendation generation.

    Args:
        hotels: Candidate hotels list.
        activities: Candidate activities list.
        intent: Structured user travel intent.

    Returns:
        RecommendationOutput containing top hotel and activity recommendations.
    """
    pass
