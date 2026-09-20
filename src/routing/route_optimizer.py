from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.routing.graph import RouteAlternative

DEFAULT_WEIGHTS: dict[str, float] = {
    "sun": 1.0,
    "greenery": 1.2,
    "sidewalk": 1.5,
    "stairs": 0.8,
    "speed": 1.0,
}


def _normalise_weights(weights: Mapping[str, float] | None) -> dict[str, float]:
    result = DEFAULT_WEIGHTS.copy()
    if weights is not None:
        for name, value in weights.items():
            if name not in result:
                continue
            numeric = float(value)
            if numeric < 0:
                raise ValueError(f"weight '{name}' must not be negative")
            result[name] = numeric
    return result


def _weighted_route_score(route: RouteAlternative, weights: Mapping[str, float]) -> float:
    speed_penalty = route.total_time_min * weights["speed"]
    sun_penalty = (100.0 - route.average_shade) * weights["sun"]
    greenery_gain = route.greenery * weights["greenery"]
    sidewalk_gain = route.sidewalk_quality * weights["sidewalk"]
    stairs_penalty = route.stairs * weights["stairs"]
    return speed_penalty + sun_penalty - greenery_gain - sidewalk_gain + stairs_penalty


def build_demo_routes(
    origin: str,
    destination: str,
    date: str,
    time: str,
    weights: Mapping[str, float] | None = None,
) -> list[dict[str, Any]]:
    """Create deterministic demo alternatives and rank them by supplied weights."""
    if not origin.strip() or not destination.strip():
        raise ValueError("origin and destination must not be blank")
    if not date.strip() or not time.strip():
        raise ValueError("date and time must not be blank")

    normalised_weights = _normalise_weights(weights)
    routes = [
        RouteAlternative(
            name="fast",
            nodes=[origin, "N1", "N2", "N3", destination],
            total_distance_km=1.4,
            total_time_min=18.0,
            average_shade=32.0,
            greenery=24.0,
            sidewalk_quality=69.0,
            stairs=1.0,
            explanation=["Небольшое расстояние", "Один из самых быстрых вариантов", "Меньше зелени и тени"],
        ),
        RouteAlternative(
            name="shaded",
            nodes=[origin, "N4", "N5", "N6", destination],
            total_distance_km=1.6,
            total_time_min=21.0,
            average_shade=76.0,
            greenery=41.0,
            sidewalk_quality=73.0,
            stairs=0.0,
            explanation=["Лучшая тень в середине дня", "На 3 минуты дольше, но заметно меньше солнечной экспозиции", "Участки с более плотной зеленью"],
        ),
        RouteAlternative(
            name="comfortable",
            nodes=[origin, "N7", "N8", "N9", destination],
            total_distance_km=1.7,
            total_time_min=23.0,
            average_shade=71.0,
            greenery=51.0,
            sidewalk_quality=91.0,
            stairs=0.0,
            explanation=["Сохранён комфортный пешеходный характер маршрута", "Больше тротуаров и зелени", "Переходы лучше интегрированы в маршрут", "Меньше риска длительного воздействия солнца"],
        ),
    ]

    route_payload = []
    for route in sorted(routes, key=lambda item: _weighted_route_score(item, normalised_weights)):
        payload = route.as_dict()
        payload.update({"date": date, "time": time, "weights": normalised_weights.copy()})
        route_payload.append(payload)
    return route_payload
