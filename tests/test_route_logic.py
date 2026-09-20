from src.comfort.comfort_model import ranking
from src.routing.route_optimizer import build_demo_routes
from src.solar.sun_model import estimate_solar_exposure


def test_demo_routes_have_alternatives():
    routes = build_demo_routes("A", "B", "2026-06-15", "08:30")
    assert len(routes) == 3
    assert {route["name"] for route in routes} == {"fast", "shaded", "comfortable"}


def test_route_entries_include_expected_fields():
    route = build_demo_routes("A", "B", "2026-06-15", "08:30")[0]
    assert {"total_time_min", "average_shade", "greenery", "stairs", "explanation"} <= route.keys()


def test_route_ranking_does_not_mutate_input():
    routes = build_demo_routes("A", "B", "2026-06-15", "08:30")
    ranked = ranking(routes, {"speed": 1, "sun": 1, "greenery": 1, "sidewalk": 1, "stairs": 1})
    assert all("comfort_score" in route for route in ranked)
    assert all("comfort_score" not in route for route in routes)


def test_weights_reject_invalid_values():
    for value in (-1, 11, float("nan"), float("inf")):
        try:
            build_demo_routes("A", "B", "2026-06-15", "08:30", {"sun": value})
        except ValueError:
            pass
        else:
            raise AssertionError("invalid weight was accepted")


def test_solar_model_rejects_invalid_input():
    invalid_cases = [
        {"date": "bad", "time": "08:30"},
        {"date": "2026-06-15", "time": "25:00"},
        {"date": "2026-06-15", "time": "08:30", "latitude": 91},
    ]
    for kwargs in invalid_cases:
        try:
            estimate_solar_exposure(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid solar input was accepted")
