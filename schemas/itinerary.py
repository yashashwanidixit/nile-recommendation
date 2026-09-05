import re
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator

TIME_REGEX = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")


class ActivityPlan(BaseModel):
    activity_id: str
    name: str
    start_time: str
    end_time: str
    estimated_cost: float = Field(ge=0.0, description="Estimated cost must be non-negative")

    @field_validator("start_time", "end_time")
    @classmethod
    def validate_time_format(cls, value: str) -> str:
        if not TIME_REGEX.match(value):
            raise ValueError(f"Time '{value}' must be in HH:MM format")
        return value


class DayPlan(BaseModel):
    day: int = Field(ge=1, description="Day number must be at least 1")
    date: date
    activities: list[ActivityPlan]


class HotelPlan(BaseModel):
    hotel_id: str
    name: str


class Itinerary(BaseModel):
    destination: str
    start_date: date
    end_date: date
    hotel: HotelPlan
    days: list[DayPlan]
    estimated_total_cost: float = Field(ge=0.0, description="Estimated total cost must be non-negative")

    @field_validator("destination")
    @classmethod
    def validate_destination_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Destination must not be empty")
        return value.strip()

    @model_validator(mode="after")
    def validate_date_range(self) -> "Itinerary":
        if self.end_date < self.start_date:
            raise ValueError("end_date must not be before start_date")
        return self


class ItineraryResponse(BaseModel):
    """Response contract for itinerary generation endpoint."""

    status: str = "not_implemented"
    message: Optional[str] = "Itinerary generation will be implemented after recommendation logic and LLM integration."
    itinerary: Optional[Itinerary] = None
