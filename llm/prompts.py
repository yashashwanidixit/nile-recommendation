from schemas.intent import UserIntent
from schemas.recommendation import RecommendationOutput


def build_itinerary_prompt(
    intent: UserIntent, recommendations: RecommendationOutput
) -> str:
    """Build the prompt for structured itinerary generation.

    Args:
        intent: Structured user travel intent.
        recommendations: Top recommendations for hotels and activities.

    Returns:
        Formatted prompt string instructing the LLM to output valid itinerary JSON.
    """
    pass
