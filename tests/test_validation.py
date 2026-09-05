import pytest
from datetime import date
from pydantic import ValidationError

from schemas.activity import Activity
from schemas.hotel import Hotel
from schemas.intent import Preferences, UserIntent
from services.data_loader import load_activities, load_hotels


# =====================================================================
# Intent Tests
# =====================================================================

def test_valid_intent_accepted():
    intent = UserIntent(
        destination="Goa",
        start_date=date(2026, 10, 10),
        end_date=date(2026, 10, 14),
        group_size=4,
        budget=40000.0,
        preferences=Preferences(
            required=["wifi"],
            preferred=["beach", "luxury", "nightlife"],
        ),
        activities=["water_sports", "nightlife"],
    )
    assert intent.destination == "Goa"
    assert intent.group_size == 4
    assert intent.budget == 40000.0
    assert len(intent.preferences.required) == 1
    assert len(intent.preferences.preferred) == 3


def test_invalid_group_size_rejected():
    with pytest.raises(ValidationError):
        UserIntent(
            destination="Goa",
            start_date=date(2026, 10, 10),
            end_date=date(2026, 10, 14),
            group_size=0,  # Invalid: must be >= 1
            budget=40000.0,
            preferences=Preferences(required=[], preferred=[]),
            activities=[],
        )


def test_negative_budget_rejected():
    with pytest.raises(ValidationError):
        UserIntent(
            destination="Goa",
            start_date=date(2026, 10, 10),
            end_date=date(2026, 10, 14),
            group_size=2,
            budget=-500.0,  # Invalid: must be >= 0
            preferences=Preferences(required=[], preferred=[]),
            activities=[],
        )


def test_invalid_date_range_rejected():
    with pytest.raises(ValidationError):
        UserIntent(
            destination="Goa",
            start_date=date(2026, 10, 14),
            end_date=date(2026, 10, 10),  # Invalid: end_date < start_date
            group_size=2,
            budget=20000.0,
            preferences=Preferences(required=[], preferred=[]),
            activities=[],
        )


def test_empty_destination_rejected():
    with pytest.raises(ValidationError):
        UserIntent(
            destination="   ",  # Invalid: empty string
            start_date=date(2026, 10, 10),
            end_date=date(2026, 10, 14),
            group_size=2,
            budget=20000.0,
            preferences=Preferences(required=[], preferred=[]),
            activities=[],
        )


# =====================================================================
# Hotel Tests
# =====================================================================

def test_valid_hotel_accepted():
    hotel = Hotel(
        hotel_id="H001",
        name="Ocean Breeze Resort",
        destination="Goa",
        location="Calangute",
        price_per_night=5000.0,
        max_guests=4,
        amenities=["pool", "wifi", "breakfast", "spa"],
        tags=["beach", "luxury", "nightlife"],
        rating=4.5,
        latitude=15.54,
        longitude=73.76,
        availability=True,
        partnered=True,
    )
    assert hotel.hotel_id == "H001"
    assert hotel.rating == 4.5
    assert hotel.max_guests == 4


def test_invalid_hotel_rating_rejected():
    # Rating > 5.0
    with pytest.raises(ValidationError):
        Hotel(
            hotel_id="H001",
            name="Ocean Breeze Resort",
            destination="Goa",
            location="Calangute",
            price_per_night=5000.0,
            max_guests=4,
            amenities=["wifi"],
            tags=["beach"],
            rating=5.5,  # Invalid: must be <= 5.0
            latitude=15.54,
            longitude=73.76,
            availability=True,
            partnered=True,
        )

    # Rating < 0.0
    with pytest.raises(ValidationError):
        Hotel(
            hotel_id="H001",
            name="Ocean Breeze Resort",
            destination="Goa",
            location="Calangute",
            price_per_night=5000.0,
            max_guests=4,
            amenities=["wifi"],
            tags=["beach"],
            rating=-1.0,  # Invalid: must be >= 0.0
            latitude=15.54,
            longitude=73.76,
            availability=True,
            partnered=True,
        )


def test_invalid_hotel_max_guests_rejected():
    with pytest.raises(ValidationError):
        Hotel(
            hotel_id="H001",
            name="Ocean Breeze Resort",
            destination="Goa",
            location="Calangute",
            price_per_night=5000.0,
            max_guests=0,  # Invalid: must be >= 1
            amenities=["wifi"],
            tags=["beach"],
            rating=4.0,
            latitude=15.54,
            longitude=73.76,
            availability=True,
            partnered=True,
        )


# =====================================================================
# Activity Tests
# =====================================================================

def test_valid_activity_accepted():
    activity = Activity(
        activity_id="A001",
        name="Baga Water Sports",
        destination="Goa",
        location="Baga",
        category="water_sports",
        price_per_person=1500.0,
        duration_hours=2.0,
        opening_time="09:00",
        closing_time="18:00",
        tags=["adventure", "beach", "water_sports"],
        suitable_for=["friends", "couples"],
        rating=4.6,
        latitude=15.55,
        longitude=73.75,
        availability=True,
    )
    assert activity.activity_id == "A001"
    assert activity.duration_hours == 2.0
    assert activity.rating == 4.6


def test_invalid_activity_rating_rejected():
    with pytest.raises(ValidationError):
        Activity(
            activity_id="A001",
            name="Baga Water Sports",
            destination="Goa",
            location="Baga",
            category="water_sports",
            price_per_person=1500.0,
            duration_hours=2.0,
            opening_time="09:00",
            closing_time="18:00",
            tags=["beach"],
            suitable_for=["friends"],
            rating=6.0,  # Invalid: > 5.0
            latitude=15.55,
            longitude=73.75,
            availability=True,
        )


def test_invalid_activity_duration_rejected():
    with pytest.raises(ValidationError):
        Activity(
            activity_id="A001",
            name="Baga Water Sports",
            destination="Goa",
            location="Baga",
            category="water_sports",
            price_per_person=1500.0,
            duration_hours=0.0,  # Invalid: must be > 0
            opening_time="09:00",
            closing_time="18:00",
            tags=["beach"],
            suitable_for=["friends"],
            rating=4.0,
            latitude=15.55,
            longitude=73.75,
            availability=True,
        )


def test_invalid_activity_time_format_rejected():
    with pytest.raises(ValidationError):
        Activity(
            activity_id="A001",
            name="Baga Water Sports",
            destination="Goa",
            location="Baga",
            category="water_sports",
            price_per_person=1500.0,
            duration_hours=2.0,
            opening_time="9:00",  # Invalid format (should be HH:MM)
            closing_time="18:00",
            tags=["beach"],
            suitable_for=["friends"],
            rating=4.0,
            latitude=15.55,
            longitude=73.75,
            availability=True,
        )


# =====================================================================
# Data Loading Tests
# =====================================================================

def test_hotels_json_loads_successfully():
    hotels = load_hotels()
    assert len(hotels) >= 1
    assert all(isinstance(h, Hotel) for h in hotels)
    assert all(h.destination == "Goa" for h in hotels)


def test_activities_json_loads_successfully():
    activities = load_activities()
    assert len(activities) >= 1
    assert all(isinstance(a, Activity) for a in activities)
    assert all(a.destination == "Goa" for a in activities)
