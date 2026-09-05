from typing import Optional

from schemas.activity import Activity
from schemas.hotel import Hotel
from schemas.intent import UserIntent
from schemas.recommendation import RecommendationItem, RecommendationOutput
from services.filtering import filter_activities, filter_hotels
from services.providers.activity_provider import (
    BaseActivityProvider,
    get_activity_provider,
)
from services.providers.hotel_provider import (
    BaseHotelProvider,
    get_hotel_provider,
)


def get_filtered_hotels(
    intent: UserIntent, provider: Optional[BaseHotelProvider] = None
) -> list[Hotel]:
    """Acquire hotels from provider and apply deterministic hard filtering.

    Pipeline:
        Hotel Provider -> list[Hotel] -> filter_hotels() -> eligible hotels

    Args:
        intent: User travel intent.
        provider: Optional hotel provider instance (defaults to active provider).

    Returns:
        List of eligible Hotel objects passing hard constraints.
    """
    p = provider or get_hotel_provider()
    raw_hotels = p.get_hotels()
    return filter_hotels(raw_hotels, intent)


def get_filtered_activities(
    intent: UserIntent, provider: Optional[BaseActivityProvider] = None
) -> list[Activity]:
    """Acquire activities from provider and apply deterministic hard filtering.

    Pipeline:
        Activity Provider -> list[Activity] -> filter_activities() -> eligible activities

    Args:
        intent: User travel intent.
        provider: Optional activity provider instance (defaults to active provider).

    Returns:
        List of eligible Activity objects passing hard constraints.
    """
    p = provider or get_activity_provider()
    raw_activities = p.get_activities()
    return filter_activities(raw_activities, intent)


def recommend_hotels(
    hotels: list[Hotel], intent: UserIntent, top_k: int = 5
) -> list[RecommendationItem]:
    """Apply hard filtering and return eligible hotels for API testing."""

    eligible_hotels = filter_hotels(hotels, intent)

    return [
        RecommendationItem(
            vendor_id=hotel.hotel_id,
            name=hotel.name,
            score=0.0,
            reasons=["Passed hard filtering constraints"],
        )
        for hotel in eligible_hotels[:top_k]
    ]


def recommend_activities(
    activities: list[Activity], intent: UserIntent, top_k: int = 5
) -> list[RecommendationItem]:
    """Apply hard filtering and return eligible activities for API testing."""

    eligible_activities = filter_activities(activities, intent)

    return [
        RecommendationItem(
            vendor_id=activity.activity_id,
            name=activity.name,
            score=0.0,
            reasons=["Passed hard filtering constraints"],
        )
        for activity in eligible_activities[:top_k]
    ]


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
