import re
from pydantic import BaseModel, ConfigDict, Field, field_validator

TIME_REGEX = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")


class Activity(BaseModel):
    model_config = ConfigDict(extra="allow")

    activity_id: str
    name: str
    destination: str
    location: str
    category: str
    price_per_person: float = Field(ge=0.0, description="Price per person must be non-negative")
    duration_hours: float = Field(gt=0.0, description="Duration in hours must be greater than 0")
    opening_time: str
    closing_time: str
    tags: list[str]
    suitable_for: list[str]
    rating: float = Field(ge=0.0, le=5.0, description="Rating must be between 0 and 5")
    latitude: float = Field(ge=-90.0, le=90.0, description="Latitude must be between -90 and 90")
    longitude: float = Field(ge=-180.0, le=180.0, description="Longitude must be between -180 and 180")
    availability: bool

    @field_validator("opening_time", "closing_time")
    @classmethod
    def validate_time_format(cls, value: str) -> str:
        if not TIME_REGEX.match(value):
            raise ValueError(f"Time '{value}' must be in HH:MM (24-hour) format")
        return value
