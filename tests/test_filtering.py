from datetime import date

from schemas.activity import Activity
from schemas.hotel import Hotel
from schemas.intent import Preferences, UserIntent
from services.data_loader import load_activities, load_hotels
from services.filtering import (
    filter_activities,
    filter_hotels,
    is_activity_eligible,
    is_hotel_eligible,
)
from services.providers.activity_provider import (
    BaseActivityProvider,
    MockActivityProvider,
    get_activities,
    get_activity_provider,
    set_activity_provider,
)
from services.providers.hotel_provider import (
    BaseHotelProvider,
    MockHotelProvider,
    get_hotel_provider,
    get_hotels,
    set_hotel_provider,
)
from services.recommendation import get_filtered_activities, get_filtered_hotels


def make_intent(
    destination: str = "Goa",
    group_size: int = 4,
    budget: float = 40000.0,
    required: list[str] | None = None,
    preferred: list[str] | None = None,
    activities: list[str] | None = None,
) -> UserIntent:
    return UserIntent(
        destination=destination,
        start_date=date(2026, 10, 10),
        end_date=date(2026, 10, 14),
        group_size=group_size,
        budget=budget,
        preferences=Preferences(
            required=required if required is not None else ["wifi"],
            preferred=preferred if preferred is not None else ["beach", "luxury"],
        ),
        activities=activities if activities is not None else ["water_sports", "nightlife"],
    )


def make_hotel(
    hotel_id: str = "H001",
    name: str = "Test Hotel",
    destination: str = "Goa",
    location: str = "Calangute",
    price_per_night: float = 5000.0,
    max_guests: int = 4,
    amenities: list[str] | None = None,
    tags: list[str] | None = None,
    rating: float = 4.5,
    latitude: float = 15.54,
    longitude: float = 73.76,
    availability: bool = True,
    partnered: bool = True,
) -> Hotel:
    return Hotel(
        hotel_id=hotel_id,
        name=name,
        destination=destination,
        location=location,
        price_per_night=price_per_night,
        max_guests=max_guests,
        amenities=amenities if amenities is not None else ["wifi", "pool"],
        tags=tags if tags is not None else ["beach"],
        rating=rating,
        latitude=latitude,
        longitude=longitude,
        availability=availability,
        partnered=partnered,
    )


def make_activity(
    activity_id: str = "A001",
    name: str = "Test Activity",
    destination: str = "Goa",
    location: str = "Baga",
    category: str = "water_sports",
    price_per_person: float = 1500.0,
    duration_hours: float = 2.0,
    opening_time: str = "09:00",
    closing_time: str = "18:00",
    tags: list[str] | None = None,
    suitable_for: list[str] | None = None,
    rating: float = 4.5,
    latitude: float = 15.55,
    longitude: float = 73.75,
    availability: bool = True,
    **extra_kwargs,
) -> Activity:
    return Activity(
        activity_id=activity_id,
        name=name,
        destination=destination,
        location=location,
        category=category,
        price_per_person=price_per_person,
        duration_hours=duration_hours,
        opening_time=opening_time,
        closing_time=closing_time,
        tags=tags if tags is not None else ["adventure", "water_sports"],
        suitable_for=suitable_for if suitable_for is not None else ["friends", "couples"],
        rating=rating,
        latitude=latitude,
        longitude=longitude,
        availability=availability,
        **extra_kwargs,
    )


# =====================================================================
# Basic interface check
# =====================================================================

def test_filter_hotel_placeholder_exists():
    assert callable(filter_hotels)


def test_filter_activity_placeholder_exists():
    assert callable(filter_activities)


# =====================================================================
# Hotel Hard Filtering Tests
# =====================================================================

def test_hotel_matching_destination_passes():
    intent = make_intent(destination="Goa")
    hotel = make_hotel(destination="Goa")
    assert is_hotel_eligible(hotel, intent) is True
    assert filter_hotels([hotel], intent) == [hotel]


def test_hotel_wrong_destination_rejected():
    intent = make_intent(destination="Goa")
    hotel = make_hotel(destination="Mumbai")
    assert is_hotel_eligible(hotel, intent) is False
    assert filter_hotels([hotel], intent) == []


def test_hotel_available_passes():
    intent = make_intent()
    hotel = make_hotel(availability=True)
    assert is_hotel_eligible(hotel, intent) is True
    assert filter_hotels([hotel], intent) == [hotel]


def test_hotel_unavailable_rejected():
    intent = make_intent()
    hotel = make_hotel(availability=False)
    assert is_hotel_eligible(hotel, intent) is False
    assert filter_hotels([hotel], intent) == []


def test_hotel_sufficient_capacity_passes():
    intent = make_intent(group_size=4)
    hotel_exact = make_hotel(max_guests=4)
    hotel_larger = make_hotel(max_guests=6)
    assert is_hotel_eligible(hotel_exact, intent) is True
    assert is_hotel_eligible(hotel_larger, intent) is True
    assert filter_hotels([hotel_exact, hotel_larger], intent) == [hotel_exact, hotel_larger]


def test_hotel_insufficient_capacity_rejected():
    intent = make_intent(group_size=4)
    hotel = make_hotel(max_guests=3)
    assert is_hotel_eligible(hotel, intent) is False
    assert filter_hotels([hotel], intent) == []


def test_hotel_required_preference_present_passes():
    intent = make_intent(required=["wifi"])
    hotel = make_hotel(amenities=["wifi", "pool"])
    assert is_hotel_eligible(hotel, intent) is True
    assert filter_hotels([hotel], intent) == [hotel]


def test_hotel_missing_required_preference_rejected():
    intent = make_intent(required=["wifi"])
    hotel = make_hotel(amenities=["pool"], tags=["beach"])
    assert is_hotel_eligible(hotel, intent) is False
    assert filter_hotels([hotel], intent) == []


def test_hotel_multiple_required_preferences_and_semantics():
    intent = make_intent(required=["wifi", "spa"])
    hotel = make_hotel(amenities=["wifi"], tags=["beach"])
    assert is_hotel_eligible(hotel, intent) is False
    assert filter_hotels([hotel], intent) == []


def test_hotel_required_preference_can_match_tags():
    intent = make_intent(required=["beach"])
    hotel = make_hotel(amenities=["pool"], tags=["beach"])
    assert is_hotel_eligible(hotel, intent) is True
    assert filter_hotels([hotel], intent) == [hotel]


def test_hotel_preferred_preferences_do_not_cause_rejection():
    intent = make_intent(required=[], preferred=["luxury", "nightlife"])
    hotel = make_hotel(amenities=["breakfast"], tags=["beach"])
    assert is_hotel_eligible(hotel, intent) is True
    assert filter_hotels([hotel], intent) == [hotel]


def test_hotel_multiple_hard_constraints():
    intent = make_intent(destination="Goa", group_size=4, required=["wifi"])
    hotel_fails_required = make_hotel(
        destination="Goa",
        availability=True,
        max_guests=4,
        amenities=["pool"],
        tags=["beach"],
    )
    assert is_hotel_eligible(hotel_fails_required, intent) is False
    assert filter_hotels([hotel_fails_required], intent) == []


def test_hotel_input_is_not_mutated():
    intent = make_intent(destination="Goa", group_size=4, required=["wifi"])
    hotel_pass = make_hotel(hotel_id="H1", destination="Goa", max_guests=4, amenities=["wifi"])
    hotel_fail = make_hotel(hotel_id="H2", destination="Mumbai", max_guests=2, amenities=[])
    original_list = [hotel_pass, hotel_fail]

    result = filter_hotels(original_list, intent)

    assert len(result) == 1
    assert result[0].hotel_id == "H1"
    # Original list unchanged
    assert len(original_list) == 2
    assert original_list[0].hotel_id == "H1"
    assert original_list[1].hotel_id == "H2"
    # Object attributes untouched
    assert hotel_pass.destination == "Goa"
    assert hotel_pass.max_guests == 4


# =====================================================================
# Activity Hard Filtering Tests
# =====================================================================

def test_activity_matching_destination_passes():
    intent = make_intent(destination="Goa")
    activity = make_activity(destination="Goa")
    assert is_activity_eligible(activity, intent) is True
    assert filter_activities([activity], intent) == [activity]


def test_activity_wrong_destination_rejected():
    intent = make_intent(destination="Goa")
    activity = make_activity(destination="Mumbai")
    assert is_activity_eligible(activity, intent) is False
    assert filter_activities([activity], intent) == []


def test_activity_available_passes():
    intent = make_intent()
    activity = make_activity(availability=True)
    assert is_activity_eligible(activity, intent) is True
    assert filter_activities([activity], intent) == [activity]


def test_activity_unavailable_rejected():
    intent = make_intent()
    activity = make_activity(availability=False)
    assert is_activity_eligible(activity, intent) is False
    assert filter_activities([activity], intent) == []


def test_activity_requested_category_passes():
    intent = make_intent(activities=["water_sports", "nightlife"])
    activity = make_activity(category="water_sports")
    assert is_activity_eligible(activity, intent) is True
    assert filter_activities([activity], intent) == [activity]


def test_activity_unrequested_category_rejected():
    intent = make_intent(activities=["water_sports", "nightlife"])
    activity = make_activity(category="sightseeing")
    assert is_activity_eligible(activity, intent) is False
    assert filter_activities([activity], intent) == []


def test_activity_multiple_requested_categories_or_semantics():
    intent = make_intent(activities=["water_sports", "nightlife"])
    act1 = make_activity(activity_id="A1", category="water_sports")
    act2 = make_activity(activity_id="A2", category="nightlife")
    act3 = make_activity(activity_id="A3", category="sightseeing")
    result = filter_activities([act1, act2, act3], intent)
    assert len(result) == 2
    assert {a.activity_id for a in result} == {"A1", "A2"}


def test_activity_capacity_does_not_automatically_reject():
    intent = make_intent(group_size=6)
    activity = make_activity(category="water_sports")
    activity.max_capacity = 2
    assert is_activity_eligible(activity, intent) is True
    assert filter_activities([activity], intent) == [activity]


def test_activity_suitable_for_does_not_cause_rejection():
    # group_size = 4, but suitable_for only specifies couples/solo - must NOT reject
    intent = make_intent(group_size=4, activities=["water_sports"])
    activity = make_activity(category="water_sports", suitable_for=["couples"])
    assert is_activity_eligible(activity, intent) is True
    assert filter_activities([activity], intent) == [activity]


def test_activity_price_does_not_cause_hard_rejection():
    # Total trip budget is 40000, but per person price * group_size exceeds it
    intent = make_intent(group_size=10, budget=10000.0, activities=["water_sports"])
    activity = make_activity(category="water_sports", price_per_person=5000.0)
    assert is_activity_eligible(activity, intent) is True
    assert filter_activities([activity], intent) == [activity]


def test_activity_input_is_not_mutated():
    intent = make_intent(activities=["water_sports"])
    act_pass = make_activity(activity_id="A1", category="water_sports")
    act_fail = make_activity(activity_id="A2", category="trekking")
    original = [act_pass, act_fail]

    result = filter_activities(original, intent)

    assert len(result) == 1
    assert result[0].activity_id == "A1"
    assert len(original) == 2
    assert original[0].activity_id == "A1"
    assert original[1].activity_id == "A2"


# =====================================================================
# Provider Abstraction Tests
# =====================================================================

def test_hotel_provider_returns_hotels():
    provider = MockHotelProvider()
    hotels = provider.get_hotels()
    assert isinstance(hotels, list)
    assert len(hotels) > 0
    assert all(isinstance(h, Hotel) for h in hotels)


def test_activity_provider_returns_activities():
    provider = MockActivityProvider()
    activities = provider.get_activities()
    assert isinstance(activities, list)
    assert len(activities) > 0
    assert all(isinstance(a, Activity) for a in activities)


def test_custom_provider_swapping():
    # Demonstrates replacing provider for testing or a future team-provided dataset
    class CustomHotelProvider(BaseHotelProvider):
        def get_hotels(self) -> list[Hotel]:
            return [make_hotel(hotel_id="CUSTOM_H1", destination="CustomLand")]

    original_provider = get_hotel_provider()
    try:
        set_hotel_provider(CustomHotelProvider())
        hotels = get_hotels()
        assert len(hotels) == 1
        assert hotels[0].hotel_id == "CUSTOM_H1"
        assert hotels[0].destination == "CustomLand"
    finally:
        set_hotel_provider(original_provider)


# =====================================================================
# Real Mock Data Integration Test
# =====================================================================

def test_real_mock_data_hotel_filtering():
    intent = make_intent(destination="Goa", group_size=3, required=["wifi"])
    hotels = load_hotels()
    assert len(hotels) > 0

    eligible = filter_hotels(hotels, intent)
    assert isinstance(eligible, list)
    assert len(eligible) > 0
    assert all(h.destination == "Goa" for h in eligible)
    assert all(h.availability is True for h in eligible)
    assert all(h.max_guests >= 3 for h in eligible)
    assert all("wifi" in (set(h.amenities).union(h.tags)) for h in eligible)


def test_real_mock_data_activity_filtering():
    intent = make_intent(destination="Goa", activities=["water_sports", "nightlife"])
    activities = load_activities()
    assert len(activities) > 0

    eligible = filter_activities(activities, intent)
    assert isinstance(eligible, list)
    assert len(eligible) > 0
    assert all(a.destination == "Goa" for a in eligible)
    assert all(a.availability is True for a in eligible)
    assert all(a.category in ["water_sports", "nightlife"] for a in eligible)


# =====================================================================
# Recommendation Service Pipeline Integration Test
# =====================================================================

def test_recommendation_service_pipeline():
    intent = make_intent(destination="Goa", group_size=2, required=["wifi"], activities=["water_sports"])
    filtered_hotels = get_filtered_hotels(intent)
    filtered_acts = get_filtered_activities(intent)

    assert isinstance(filtered_hotels, list)
    assert isinstance(filtered_acts, list)
    assert len(filtered_hotels) > 0
    assert len(filtered_acts) > 0
