from services.scoring import score_activities, score_hotels


def test_score_hotels_placeholder_exists():
    assert callable(score_hotels)


def test_score_activities_placeholder_exists():
    assert callable(score_activities)
