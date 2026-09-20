from fastapi.testclient import TestClient

from app.main import app
from src.routing.route_optimizer import build_demo_routes


def test_demo_routes_have_alternatives():
    routes = build_demo_routes("A", "B", "2026-06-15", "08:30")
    assert len(routes) == 3
    assert {route["name"] for route in routes} == {"fast", "shaded", "comfortable"}


def test_route_entries_include_expected_fields():
    route = build_demo_routes("A", "B", "2026-06-15", "08:30")[0]
    assert {"total_time_min", "average_shade", "greenery", "stairs", "explanation"} <= route.keys()


def test_route_ranking_does_not_mutate_input():
    routes = build_demo_routes("A", "B", "2026-06-15", "08:30")
    original = [dict(route) for route in routes]
    from src.comfort.comfort_model import ranking

    ranked = ranking(routes, {"speed": 1, "sun": 1, "greenery": 1, "sidewalk": 1, "stairs": 1})
    assert all("comfort_score" in route for route in ranked)
    assert all("comfort_score" not in route for route in original)


def test_api_validates_route_input():
    client = TestClient(app)
    response = client.post("/routes", json={"origin": "", "destination": "B"})
    assert response.status_code == 422


def test_api_returns_iso_date_and_time():
    client = TestClient(app)
    response = client.post("/routes", json={"date": "2026-06-15", "time": "08:30"})
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == "2026-06-15"
    assert body["time"] == "08:30"


def test_route_names_are_sorted_by_weighted_priority():
    routes = build_demo_routes(
        "A", "B", "2026-06-15", "08:30",
        {"sun": 1.0, "greenery": 1.4, "sidewalk": 1.2, "stairs": 0.5, "speed": 1.0},
    )
    assert len(routes) == 3
    assert all(route["weights"]["sun"] == 1.0 for route in routes)
