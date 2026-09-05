from schemas.recommendation import RecommendationItem, RecommendationOutput
from services.recommendation import (
    get_recommendations,
    recommend_activities,
    recommend_hotels,
)


def test_recommendation_item_schema():
    item = RecommendationItem(
        vendor_id="H001",
        name="Ocean Breeze Resort",
        score=0.92,
        reasons=["Direct beach access", "High rating"],
    )
    assert item.vendor_id == "H001"
    assert item.score == 0.92
    assert len(item.reasons) == 2


def test_recommendation_output_schema():
    output = RecommendationOutput(
        hotel_recommendations=[
            RecommendationItem(
                vendor_id="H001",
                name="Ocean Breeze Resort",
                score=0.92,
                reasons=["Direct beach access"],
            )
        ],
        activity_recommendations=[
            RecommendationItem(
                vendor_id="A001",
                name="Baga Water Sports",
                score=0.88,
                reasons=["Matches category"],
            )
        ],
    )
    assert len(output.hotel_recommendations) == 1
    assert len(output.activity_recommendations) == 1


def test_recommendation_functions_exist():
    assert callable(recommend_hotels)
    assert callable(recommend_activities)
    assert callable(get_recommendations)
