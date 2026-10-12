from fastapi import APIRouter, Depends

from schemas.activity import Activity
from schemas.hotel import Hotel
from schemas.intent import UserIntent
from schemas.recommendation import (
    ActivityRecommendationResponse,
    HotelRecommendationResponse,
)
from services import get_activities, get_hotels
from services.recommendation import recommend_activities, recommend_hotels

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/hotels", response_model=HotelRecommendationResponse)
def get_hotel_recommendations(
    intent: UserIntent,
    hotels: list[Hotel] = Depends(get_hotels),
) -> HotelRecommendationResponse:
    """Generate ranked hotel recommendations based on user travel intent."""
    recommendations = recommend_hotels(hotels=hotels, intent=intent)
    return HotelRecommendationResponse(
        status="received",
        recommendation_type="hotels",
        destination=intent.destination,
        group_size=intent.group_size,
        budget=intent.budget,
        recommendations=recommendations or [],
    )


@router.post("/activities", response_model=ActivityRecommendationResponse)
def get_activity_recommendations(
    intent: UserIntent,
    activities: list[Activity] = Depends(get_activities),
) -> ActivityRecommendationResponse:
    """Generate ranked activity recommendations based on user travel intent."""
    recommendations = recommend_activities(activities=activities, intent=intent)
    return ActivityRecommendationResponse(
        status="received",
        recommendation_type="activities",
        destination=intent.destination,
        requested_activities=intent.activities,
        recommendations=recommendations or [],
    )
