from datetime import date
import pytest
from pydantic import ValidationError

from schemas.itinerary import ActivityPlan, DayPlan, HotelPlan, Itinerary
from services.itinerary import generate_itinerary


def test_valid_itinerary_accepted():
    itinerary = Itinerary(
        destination="Goa",
        start_date=date(2026, 10, 10),
        end_date=date(2026, 10, 12),
        hotel=HotelPlan(hotel_id="H001", name="Ocean Breeze Resort"),
        days=[
            DayPlan(
                day=1,
                date=date(2026, 10, 10),
                activities=[
                    ActivityPlan(
                        activity_id="A001",
                        name="Baga Water Sports",
                        start_time="10:00",
                        end_time="12:00",
                        estimated_cost=1500.0,
                    )
                ],
            )
        ],
        estimated_total_cost=6500.0,
    )
    assert itinerary.destination == "Goa"
    assert len(itinerary.days) == 1
    assert itinerary.hotel.hotel_id == "H001"


def test_invalid_itinerary_date_range():
    with pytest.raises(ValidationError):
        Itinerary(
            destination="Goa",
            start_date=date(2026, 10, 12),
            end_date=date(2026, 10, 10),  # Invalid: end before start
            hotel=HotelPlan(hotel_id="H001", name="Ocean Breeze Resort"),
            days=[],
            estimated_total_cost=0.0,
        )


def test_invalid_activity_plan_time():
    with pytest.raises(ValidationError):
        ActivityPlan(
            activity_id="A001",
            name="Baga Water Sports",
            start_time="10:0",  # Invalid time format
            end_time="12:00",
            estimated_cost=1500.0,
        )


def test_itinerary_function_exists():
    assert callable(generate_itinerary)
