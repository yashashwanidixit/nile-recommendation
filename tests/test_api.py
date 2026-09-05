from unittest.mock import patch
from datetime import date
from fastapi.testclient import TestClient

from main import app
from schemas.itinerary import ActivityPlan, DayPlan, HotelPlan, Itinerary
from schemas.recommendation import RecommendationItem, RecommendationOutput
from services.data_loader import get_activities, get_hotels

client = TestClient(app)

VALID_INTENT_PAYLOAD = {
    "destination": "Goa",
    "start_date": "2026-10-10",
    "end_date": "2026-10-14",
    "group_size": 4,
    "budget": 40000,
    "preferences": {
        "required": ["wifi"],
        "preferred": ["beach", "luxury", "nightlife"],
    },
    "activities": ["water_sports", "nightlife"],
}

INVALID_INTENT_PAYLOAD = {
    "destination": "Goa",
    "start_date": "2026-10-10",
    "end_date": "2026-10-14",
    "group_size": -2,
    "budget": 40000,
    "preferences": {
        "required": ["wifi"],
        "preferred": ["beach"],
    },
    "activities": ["water_sports"],
}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "nile-recommendation",
    }


def test_hotel_recommendations_valid():
    response = client.post("/recommendations/hotels", json=VALID_INTENT_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"
    assert data["recommendation_type"] == "hotels"
    assert data["destination"] == "Goa"
    assert data["group_size"] == 4
    assert data["budget"] == 40000.0


def test_activity_recommendations_valid():
    response = client.post("/recommendations/activities", json=VALID_INTENT_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"
    assert data["recommendation_type"] == "activities"
    assert data["destination"] == "Goa"
    assert data["requested_activities"] == ["water_sports", "nightlife"]


def test_itinerary_generate_valid():
    response = client.post("/itinerary/generate", json=VALID_INTENT_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "not_implemented"
    assert "message" in data


def test_invalid_intent_rejected_with_422():
    response = client.post("/recommendations/hotels", json=INVALID_INTENT_PAYLOAD)
    assert response.status_code == 422


# =====================================================================
# Architecture & Hygiene Tests (Wiring, Caching, CORS)
# =====================================================================

def test_cors_headers_on_response():
    response = client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "*"


def test_hotel_route_invokes_service_and_formats_items():
    mock_items = [
        RecommendationItem(
            vendor_id="H001",
            name="Ocean Breeze Resort",
            score=0.95,
            reasons=["Top beach access", "High rating"],
        )
    ]
    with patch("api.routes.recommendations.recommend_hotels", return_value=mock_items) as mock_call:
        response = client.post("/recommendations/hotels", json=VALID_INTENT_PAYLOAD)
        assert response.status_code == 200
        mock_call.assert_called_once()
        data = response.json()
        assert len(data["recommendations"]) == 1
        assert data["recommendations"][0]["vendor_id"] == "H001"


def test_activity_route_invokes_service_and_formats_items():
    mock_items = [
        RecommendationItem(
            vendor_id="A001",
            name="Scuba Diving Adventure",
            score=0.92,
            reasons=["Matches category preference"],
        )
    ]
    with patch("api.routes.recommendations.recommend_activities", return_value=mock_items) as mock_call:
        response = client.post("/recommendations/activities", json=VALID_INTENT_PAYLOAD)
        assert response.status_code == 200
        mock_call.assert_called_once()
        data = response.json()
        assert len(data["recommendations"]) == 1
        assert data["recommendations"][0]["vendor_id"] == "A001"


def test_itinerary_route_invokes_services_and_returns_completed_plan():
    mock_recs = RecommendationOutput(hotel_recommendations=[], activity_recommendations=[])
    mock_itinerary = Itinerary(
        destination="Goa",
        start_date=date(2026, 10, 10),
        end_date=date(2026, 10, 14),
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

    with patch("api.routes.itinerary.get_recommendations", return_value=mock_recs) as mock_get_recs, \
         patch("api.routes.itinerary.generate_itinerary_service", return_value=mock_itinerary) as mock_gen_itin:
        response = client.post("/itinerary/generate", json=VALID_INTENT_PAYLOAD)
        assert response.status_code == 200
        mock_get_recs.assert_called_once()
        mock_gen_itin.assert_called_once()
        data = response.json()
        assert data["status"] == "success"
        assert data["itinerary"]["destination"] == "Goa"
        assert data["itinerary"]["hotel"]["hotel_id"] == "H001"


def test_data_cache_dependency_reuse():
    hotels = get_hotels()
    assert len(hotels) > 0
    # Calling dependency again should return identical cached list instance
    assert get_hotels() is hotels

    activities = get_activities()
    assert len(activities) > 0
    assert get_activities() is activities
