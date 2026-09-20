from __future__ import annotations

from collections.abc import Mapping
from math import isfinite
from typing import Any

from src.routing.graph import RouteAlternative

DEFAULT_WEIGHTS: dict[str, float] = {
    "sun": 1.0,
    "greenery": 1.2,
    "sidewalk": 1.5,
    "stairs": 0.8,
    "speed": 1.0,
}
MAX_WEIGHT = 10.0


def _normalise_weights(weights: Mapping[str, float] | None) -> dict[str, float]:
    result = DEFAULT_WEIGHTS.copy()
    if weights is not None:
        for name, value in weights.items():
            if name not in result:
                continue
            numeric = float(value)
            if not isfinite(numeric) or not 0.0 <= numeric <= MAX_WEIGHT:
                raise ValueError(f"weight '{name}' must be finite and between 0 and {MAX_WEIGHT}")
            result[name] = numeric
    return result


def _weighted_route_score(route: RouteAlternative, weights: Mapping[str, float]) -> float:
    return (
        route.total_time_min * weights["speed"]
        + (100.0 - route.average_shade) * weights["sun"]
        - route.greenery * weights["greenery"]
        - route.sidewalk_quality * weights["sidewalk"]
        + route.stairs * weights["stairs"]
    )


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
            "fast", [origin, "N1", "N2", "N3", destination], 1.4, 18.0, 32.0, 24.0, 69.0, 1.0,
            explanation=["Небольшое расстояние", "Один из самых быстрых вариантов", "Меньше зелени и тени"],
        ),
        RouteAlternative(
            "shaded", [origin, "N4", "N5", "N6", destination], 1.6, 21.0, 76.0, 41.0, 73.0, 0.0,
            explanation=["Лучшая тень в середине дня", "На 3 минуты дольше, но заметно меньше солнечной экспозиции", "Участки с более плотной зеленью"],
        ),
        RouteAlternative(
            "comfortable", [origin, "N7", "N8", "N9", destination], 1.7, 23.0, 71.0, 51.0, 91.0, 0.0,
            explanation=["Сохранён комфортный пешеходный характер маршрута", "Больше тротуаров и зелени", "Переходы лучше интегрированы в маршрут", "Меньше риска длительного воздействия солнца"],
        ),
    ]
    result: list[dict[str, Any]] = []
    for route in sorted(routes, key=lambda item: _weighted_route_score(item, normalised_weights)):
        payload = route.as_dict()
        payload.update({"date": date, "time": time, "weights": normalised_weights.copy()})
        result.append(payload)
    return result
