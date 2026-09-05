from schemas.itinerary import Itinerary


def parse_itinerary_response(response_text: str) -> Itinerary:
    """Parse raw LLM response text into a validated Itinerary model.

    Args:
        response_text: Raw LLM output containing JSON text.

    Returns:
        Validated Itinerary instance.
    """
    pass
