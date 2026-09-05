from fastapi import APIRouter
from schemas.intent import UserIntent
from services.recommendation import get_filtered_activities, get_filtered_hotels

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/hotels")
def get_hotel_recommendations(intent: UserIntent) -> dict:
    """Receive and validate travel intent, returning temporary hotel response."""
    # Executes service pipeline: provider -> filtering
    _ = get_filtered_hotels(intent)

    return {
        "status": "received",
        "recommendation_type": "hotels",
        "destination": intent.destination,
        "group_size": intent.group_size,
        "budget": intent.budget,
    }


@router.post("/activities")
def get_activity_recommendations(intent: UserIntent) -> dict:
    """Receive and validate travel intent, returning temporary activity response."""
    # Executes service pipeline: provider -> filtering
    _ = get_filtered_activities(intent)

    return {
        "status": "received",
        "recommendation_type": "activities",
        "destination": intent.destination,
        "requested_activities": intent.activities,
    }
