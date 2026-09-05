from fastapi import APIRouter, Depends

from schemas.activity import Activity
from schemas.hotel import Hotel
from schemas.intent import UserIntent
from schemas.itinerary import ItineraryResponse
from services.data_loader import get_activities, get_hotels
from services.itinerary import generate_itinerary as generate_itinerary_service
from services.recommendation import get_recommendations

router = APIRouter(prefix="/itinerary", tags=["itinerary"])


@router.post("/generate", response_model=ItineraryResponse)
def generate_itinerary(
    intent: UserIntent,
    hotels: list[Hotel] = Depends(get_hotels),
    activities: list[Activity] = Depends(get_activities),
) -> ItineraryResponse:
    """Generate structured travel itinerary using recommendations and LLM orchestration."""
    recommendations = get_recommendations(hotels=hotels, activities=activities, intent=intent)
    itinerary = generate_itinerary_service(intent=intent, recommendations=recommendations)

    if itinerary is not None:
        return ItineraryResponse(
            status="success",
            message=None,
            itinerary=itinerary,
        )

    return ItineraryResponse(
        status="not_implemented",
        message="Itinerary generation will be implemented after recommendation logic and LLM integration.",
        itinerary=None,
    )
