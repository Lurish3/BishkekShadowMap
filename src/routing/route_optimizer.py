from __future__ import annotations

from typing import Dict, List

from src.routing.graph import RouteAlternative


def _weighted_route_score(route: RouteAlternative, weights: Dict[str, float]) -> float:
    speed_penalty = route.total_time_min * weights.get("speed", 1.0)
    sun_penalty = (100.0 - route.average_shade) * weights.get("sun", 1.0)
    greenery_gain = route.greenery * weights.get("greenery", 1.0)
    sidewalk_gain = route.sidewalk_quality * weights.get("sidewalk", 1.0)
    stairs_penalty = route.explanation.count("stairs") * weights.get("stairs", 1.0)

    return speed_penalty + sun_penalty - greenery_gain - sidewalk_gain + stairs_penalty


def build_demo_routes(
    origin: str,
    destination: str,
    date: str,
    time: str,
    weights: Dict[str, float] | None = None,
) -> List[Dict[str, object]]:
    """Create route alternatives for a simple demo corridor."""
    weights = weights or {"sun": 1.0, "greenery": 1.2, "sidewalk": 1.5, "stairs": 0.8, "speed": 1.0}

    fast = RouteAlternative(
        name="fast",
        nodes=[origin, "N1", "N2", "N3", destination],
        total_distance_km=1.4,
        total_time_min=18.0,
        average_shade=32.0,
        greenery=24.0,
        sidewalk_quality=69.0,
        explanation=[
            "Небольшое расстояние",
            "Один из самых быстрых вариантов",
            "Меньше зелени и тени",
        ],
    )

    shaded = RouteAlternative(
        name="shaded",
        nodes=[origin, "N4", "N5", "N6", destination],
        total_distance_km=1.6,
        total_time_min=21.0,
        average_shade=76.0,
        greenery=41.0,
        sidewalk_quality=73.0,
        explanation=[
            "Лучшая тень в середине дня",
            "На 3 минуты дольше, но заметно меньше солнечной экспозиции",
            "Участки с более плотной зеленью",
        ],
    )

    comfortable = RouteAlternative(
        name="comfortable",
        nodes=[origin, "N7", "N8", "N9", destination],
        total_distance_km=1.7,
        total_time_min=23.0,
        average_shade=71.0,
        greenery=51.0,
        sidewalk_quality=91.0,
        explanation=[
            "Сохранён комфортный пешеходный характер маршрута",
            "Больше тротуаров и зелени",
            "Переходы лучше интегрированы в маршрут",
            "Меньше риска длительного воздействия солнца",
        ],
    )

    routes = [fast, shaded, comfortable]
    sorted_routes = sorted(routes, key=lambda route: _weighted_route_score(route, weights))
    route_payload = [route.as_dict() for route in sorted_routes]

    for route in route_payload:
        route["date"] = date
        route["time"] = time
        route["weights"] = weights

    return route_payload
