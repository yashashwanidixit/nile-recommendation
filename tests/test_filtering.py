from services.filtering import filter_activities, filter_hotels


def test_filter_hotel_placeholder_exists():
    assert callable(filter_hotels)


def test_filter_activity_placeholder_exists():
    assert callable(filter_activities)
