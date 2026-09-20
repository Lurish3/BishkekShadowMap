from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def _as_float(route: Mapping[str, Any], key: str) -> float:
    value = route.get(key, 0.0)
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"route field '{key}' must be numeric") from exc


def comfort_score(route: Mapping[str, Any], weights: Mapping[str, float]) -> float:
    """Return a lower-is-better score without mutating the route."""
    return round(
        _as_float(route, "total_time_min") * float(weights.get("speed", 1.0))
        + (100.0 - _as_float(route, "average_shade")) * float(weights.get("sun", 1.0))
        - _as_float(route, "greenery") * float(weights.get("greenery", 1.0))
        - _as_float(route, "sidewalk_quality") * float(weights.get("sidewalk", 1.0)) * 0.2
        + _as_float(route, "stairs") * float(weights.get("stairs", 1.0)) * 5.0,
        2,
    )


def explain_tradeoff(base_route: Mapping[str, Any], candidate_route: Mapping[str, Any]) -> str:
    time_delta = _as_float(candidate_route, "total_time_min") - _as_float(base_route, "total_time_min")
    shade_delta = _as_float(candidate_route, "average_shade") - _as_float(base_route, "average_shade")
    sidewalk_delta = _as_float(candidate_route, "sidewalk_quality") - _as_float(base_route, "sidewalk_quality")
    greenery_delta = _as_float(candidate_route, "greenery") - _as_float(base_route, "greenery")
    return (
        f"Время: {time_delta:+.1f} мин; "
        f"Тень: {shade_delta:+.1f}%; "
        f"Тротуары: {sidewalk_delta:+.1f}%; "
        f"Зелень: {greenery_delta:+.1f}%"
    )


def ranking(routes: list[dict[str, Any]], weights: Mapping[str, float]) -> list[dict[str, Any]]:
    """Return copied route records sorted by score."""
    return sorted(
        (dict(route, comfort_score=comfort_score(route, weights)) for route in routes),
        key=lambda item: item["comfort_score"],
    )
