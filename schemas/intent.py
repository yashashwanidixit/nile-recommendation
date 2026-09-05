from datetime import date
from pydantic import BaseModel, Field, field_validator, model_validator


class Preferences(BaseModel):
    required: list[str]
    preferred: list[str]


class UserIntent(BaseModel):
    destination: str
    start_date: date
    end_date: date
    group_size: int = Field(ge=1, description="Group size must be at least 1")
    budget: float = Field(ge=0.0, description="Budget must be non-negative")
    preferences: Preferences
    activities: list[str]

    @field_validator("destination")
    @classmethod
    def validate_destination_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Destination must not be empty")
        return value.strip()

    @model_validator(mode="after")
    def validate_date_range(self) -> "UserIntent":
        if self.end_date < self.start_date:
            raise ValueError("end_date must not be before start_date")
        return self
