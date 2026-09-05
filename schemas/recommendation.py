from pydantic import BaseModel, Field


class RecommendationItem(BaseModel):
    vendor_id: str
    name: str
    score: float
    reasons: list[str]


class RecommendationOutput(BaseModel):
    hotel_recommendations: list[RecommendationItem]
    activity_recommendations: list[RecommendationItem]


class HotelRecommendationResponse(BaseModel):
    """Response contract for hotel recommendation endpoint."""

    status: str = "received"
    recommendation_type: str = "hotels"
    destination: str
    group_size: int
    budget: float
    recommendations: list[RecommendationItem] = Field(default_factory=list)


class ActivityRecommendationResponse(BaseModel):
    """Response contract for activity recommendation endpoint."""

    status: str = "received"
    recommendation_type: str = "activities"
    destination: str
    requested_activities: list[str]
    recommendations: list[RecommendationItem] = Field(default_factory=list)
