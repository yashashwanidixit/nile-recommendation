from schemas.intent import UserIntent
from schemas.itinerary import Itinerary
from schemas.recommendation import RecommendationOutput


def generate_itinerary(
    intent: UserIntent, recommendations: RecommendationOutput
) -> Itinerary:
    """Generate an itinerary using the LLM layer.

    Coordinates prompt construction, LLM generation, and parsing into
    the structured Itinerary schema.

    Args:
        intent: Structured user travel intent.
        recommendations: Top recommendations for hotels and activities.

    Returns:
        Structured Itinerary instance.
    """
    pass
