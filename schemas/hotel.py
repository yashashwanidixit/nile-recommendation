from pydantic import BaseModel, Field


class Hotel(BaseModel):
    hotel_id: str
    name: str
    destination: str
    location: str
    price_per_night: float = Field(ge=0.0, description="Price per night must be non-negative")
    max_guests: int = Field(ge=1, description="Maximum guests must be at least 1")
    amenities: list[str]
    tags: list[str]
    rating: float = Field(ge=0.0, le=5.0, description="Rating must be between 0 and 5")
    latitude: float = Field(ge=-90.0, le=90.0, description="Latitude must be between -90 and 90")
    longitude: float = Field(ge=-180.0, le=180.0, description="Longitude must be between -180 and 180")
    availability: bool
    partnered: bool
