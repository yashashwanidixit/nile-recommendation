from fastapi import APIRouter
from schemas.intent import UserIntent

router = APIRouter(prefix="/itinerary", tags=["itinerary"])


@router.post("/generate")
def generate_itinerary(intent: UserIntent) -> dict:
    """Receive and validate travel intent, returning placeholder itinerary response."""
    return {
        "status": "not_implemented",
        "message": "Itinerary generation will be implemented after recommendation logic and LLM integration.",
    }
