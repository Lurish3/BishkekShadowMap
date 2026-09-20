from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def _number(route: Mapping[str, Any], key: str) -> float:
    value = route.get(key, 0.0)
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"route field '{key}' must be numeric") from exc


def comfort_score(route: Mapping[str, Any], weights: Mapping[str, float]) -> float:
    """Return a lower-is-better score without mutating the route."""
    travel_time = _number(route, "total_time_min")
    shade = _number(route, "average_shade")
    greenery = _number(route, "greenery")
    sidewalk_quality = _number(route, "sidewalk_quality")
    stairs = _number(route, "stairs")
    return round(
        travel_time * float(weights.get("speed", 1.0))
        + (100.0 - shade) * float(weights.get("sun", 1.0))
        - greenery * float(weights.get("greenery", 1.0))
        - sidewalk_quality * float(weights.get("sidewalk", 1.0)) * 0.2
        + stairs * float(weights.get("stairs", 1.0)) * 5.0,
        2,
    )


def explain_tradeoff(base_route: Mapping[str, Any], candidate_route: Mapping[str, Any]) -> str:
    time_delta = _number(candidate_route, "total_time_min") - _number(base_route, "total_time_min")
    shade_delta = _number(candidate_route, "average_shade") - _number(base_route, "average_shade")
    sidewalk_delta = _number(candidate_route, "sidewalk_quality") - _number(base_route, "sidewalk_quality")
    greenery_delta = _number(candidate_route, "greenery") - _number(base_route, "greenery")
    return (
        f"Время: {time_delta:+.1f} мин; "
        f"Тень: {shade_delta:+.1f}%; "
        f"Тротуары: {sidewalk_delta:+.1f}%; "
        f"Зелень: {greenery_delta:+.1f}%"
    )


def ranking(routes: list[dict[str, Any]], weights: Mapping[str, float]) -> list[dict[str, Any]]:
    """Return copied route records sorted by score."""
    ranked = [dict(route, comfort_score=comfort_score(route, weights)) for route in routes]
    return sorted(ranked, key=lambda item: item["comfort_score"])
