from fastapi.testclient import TestClient
from main import app

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
