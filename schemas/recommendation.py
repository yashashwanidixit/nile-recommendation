from pydantic import BaseModel


class RecommendationItem(BaseModel):
    vendor_id: str
    name: str
    score: float
    reasons: list[str]


class RecommendationOutput(BaseModel):
    hotel_recommendations: list[RecommendationItem]
    activity_recommendations: list[RecommendationItem]
