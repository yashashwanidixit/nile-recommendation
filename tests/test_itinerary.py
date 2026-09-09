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
        hotel=HotelPlan(
            hotel_id="H001",
            name="Ocean Breeze Resort",
            location="Calangute",
            price_per_night=3500.0,
            user_preferences=["beach", "pool"],
        ),
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
                        category="water_sports",
                        location="Baga Beach",
                        user_preferences=["water_sports"],
                    )
                ],
            )
        ],
        estimated_total_cost=6500.0,
    )
    assert itinerary.destination == "Goa"
    assert len(itinerary.days) == 1
    assert itinerary.hotel.hotel_id == "H001"
    assert itinerary.hotel.location == "Calangute"
    assert itinerary.hotel.price_per_night == 3500.0
    assert itinerary.hotel.price == 3500.0
    assert itinerary.hotel.user_preferences == ["beach", "pool"]
    assert itinerary.days[0].activities[0].category == "water_sports"
    assert itinerary.days[0].activities[0].location == "Baga Beach"
    assert itinerary.days[0].activities[0].user_preferences == ["water_sports"]
    assert itinerary.days[0].activities[0].price == 1500.0


def test_invalid_itinerary_date_range():
    with pytest.raises(ValidationError):
        Itinerary(
            destination="Goa",
            start_date=date(2026, 10, 12),
            end_date=date(2026, 10, 10),  # Invalid: end before start
            hotel=HotelPlan(
                hotel_id="H001",
                name="Ocean Breeze Resort",
                location="Calangute",
                price_per_night=3500.0,
            ),
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
            category="water_sports",
            location="Baga Beach",
        )


def test_hotel_plan_extended_fields_validation():
    # Valid hotel plan with all fields
    hp = HotelPlan(
        hotel_id="H002",
        name="Amber Bungalows",
        location="Panaji",
        price_per_night=1776.0,
        category="hotel",
        user_preferences=["central", "wifi"],
    )
    assert hp.hotel_id == "H002"
    assert hp.location == "Panaji"
    assert hp.price_per_night == 1776.0
    assert hp.price == 1776.0
    assert hp.category == "hotel"
    assert hp.user_preferences == ["central", "wifi"]

    # Valid hotel plan with price alias
    hp_alias = HotelPlan(
        hotel_id="H002",
        name="Amber Bungalows",
        price=1776.0,
    )
    assert hp_alias.price_per_night == 1776.0
    assert hp_alias.price == 1776.0

    # Underlying hotel data gap: category defaults to None
    hp_defaults = HotelPlan(hotel_id="H003", name="Default Hotel")
    assert hp_defaults.location is None
    assert hp_defaults.price_per_night is None
    assert hp_defaults.category is None
    assert hp_defaults.user_preferences is None

    # Negative price per night rejected
    with pytest.raises(ValidationError):
        HotelPlan(hotel_id="H004", name="Invalid Price", price_per_night=-100.0)


def test_activity_plan_extended_fields_validation():
    # Valid activity plan with all fields
    ap = ActivityPlan(
        activity_id="A002",
        name="Old Goa Churches Tour",
        start_time="09:00",
        end_time="11:30",
        estimated_cost=500.0,
        category="culture",
        location="Old Goa",
        user_preferences=["sightseeing", "history"],
    )
    assert ap.activity_id == "A002"
    assert ap.category == "culture"
    assert ap.location == "Old Goa"
    assert ap.user_preferences == ["sightseeing", "history"]
    assert ap.price == 500.0

    # Defaults check
    ap_defaults = ActivityPlan(
        activity_id="A003",
        name="Minimal Activity",
        start_time="14:00",
        end_time="15:00",
        estimated_cost=0.0,
    )
    assert ap_defaults.category is None
    assert ap_defaults.location is None
    assert ap_defaults.user_preferences is None

    # Negative cost rejected
    with pytest.raises(ValidationError):
        ActivityPlan(
            activity_id="A004",
            name="Negative Cost",
            start_time="10:00",
            end_time="11:00",
            estimated_cost=-50.0,
        )


def test_itinerary_serialization_includes_extended_fields():
    itinerary = Itinerary(
        destination="Goa",
        start_date=date(2026, 10, 10),
        end_date=date(2026, 10, 12),
        hotel=HotelPlan(
            hotel_id="H001",
            name="Ocean Breeze Resort",
            location="Calangute",
            price_per_night=3500.0,
            category=None,
            user_preferences=["beach"],
        ),
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
                        category="water_sports",
                        location="Baga Beach",
                        user_preferences=["adventure"],
                    )
                ],
            )
        ],
        estimated_total_cost=6500.0,
    )

    dump = itinerary.model_dump()
    # Hotel fields check
    assert "location" in dump["hotel"]
    assert dump["hotel"]["location"] == "Calangute"
    assert "price_per_night" in dump["hotel"]
    assert dump["hotel"]["price_per_night"] == 3500.0
    assert "category" in dump["hotel"]
    assert dump["hotel"]["category"] is None
    assert "user_preferences" in dump["hotel"]
    assert dump["hotel"]["user_preferences"] == ["beach"]

    # Activity fields check
    act_dump = dump["days"][0]["activities"][0]
    assert "category" in act_dump
    assert act_dump["category"] == "water_sports"
    assert "location" in act_dump
    assert act_dump["location"] == "Baga Beach"
    assert "user_preferences" in act_dump
    assert act_dump["user_preferences"] == ["adventure"]
    assert "estimated_cost" in act_dump
    assert act_dump["estimated_cost"] == 1500.0


def test_itinerary_function_exists():
    assert callable(generate_itinerary)
