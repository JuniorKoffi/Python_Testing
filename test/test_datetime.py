import pytest
from datetime import datetime

@pytest.fixture
def competitions():
    return [
        {"name": "Spring Festival", "date": "2024-03-27 10:00:00", "numberOfPlaces": "25"},
        {"name": "Fall Classic", "date": "2024-10-22 13:30:00", "numberOfPlaces": "13"},
    ]

def test_with_old_date(competitions):
    today = datetime.now()
    comps = [competition for competition in competitions if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") < today]
    expected_comp = []
    assert comps == expected_comp

def test_competition(competitions):
    today = datetime.now()
    comps = [competition for competition in competitions if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
    expected_comps = [
        {"name": "Spring Festival", "date": "2024-03-27 10:00:00", "numberOfPlaces": "25"},
        {"name": "Fall Classic", "date": "2024-10-22 13:30:00", "numberOfPlaces": "13"},
    ]
    assert comps == expected_comps
