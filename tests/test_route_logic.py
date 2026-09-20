from src.routing.route_optimizer import build_demo_routes


def test_demo_routes_have_alternatives():
    routes = build_demo_routes("A", "B", "2026-06-15", "08:30")
    assert len(routes) == 3
    assert {route["name"] for route in routes} == {"fast", "shaded", "comfortable"}


def test_route_entries_include_expected_fields():
    routes = build_demo_routes("A", "B", "2026-06-15", "08:30")
    first = routes[0]
    assert "total_time_min" in first
    assert "average_shade" in first
    assert "greenery" in first
    assert "explanation" in first


def test_route_names_are_sorted_by_weighted_priority():
    routes = build_demo_routes("A", "B", "2026-06-15", "08:30", {"sun": 1.0, "greenery": 1.4, "sidewalk": 1.2, "stairs": 0.5, "speed": 1.0})
    names = [route["name"] for route in routes]
    assert names[0] in {"fast", "shaded", "comfortable"}
    assert len(names) == 3
