from __future__ import annotations

from typing import Dict, List


def comfort_score(route: Dict[str, object], weights: Dict[str, float]) -> float:
    time_weight = weights.get("speed", 1.0)
    sun_weight = weights.get("sun", 1.0)
    greenery_weight = weights.get("greenery", 1.0)
    sidewalk_weight = weights.get("sidewalk", 1.0)
    stairs_weight = weights.get("stairs", 1.0)

    travel_time = float(route.get("total_time_min", 0.0))
    shade = float(route.get("average_shade", 0.0))
    greenery = float(route.get("greenery", 0.0))
    sidewalk_quality = float(route.get("sidewalk_quality", 0.0))
    explanation = route.get("explanation", [])
    stairs_penalty = 1.0 if "stairs" in " ".join(explanation).lower() else 0.0

    score = (
        travel_time * time_weight
        + (100.0 - shade) * sun_weight
        - greenery * greenery_weight
        - sidewalk_quality * sidewalk_weight * 0.2
        + stairs_penalty * stairs_weight * 5.0
    )
    return round(score, 2)


def explain_tradeoff(base_route: Dict[str, object], candidate_route: Dict[str, object]) -> str:
    time_delta = float(candidate_route.get("total_time_min", 0.0)) - float(base_route.get("total_time_min", 0.0))
    shade_delta = float(candidate_route.get("average_shade", 0.0)) - float(base_route.get("average_shade", 0.0))
    sidewalk_delta = float(candidate_route.get("sidewalk_quality", 0.0)) - float(base_route.get("sidewalk_quality", 0.0))
    greenery_delta = float(candidate_route.get("greenery", 0.0)) - float(base_route.get("greenery", 0.0))

    return (
        f"Время: {time_delta:+.1f} мин; "
        f"Тень: {shade_delta:+.1f}% ; "
        f"Тротуары: {sidewalk_delta:+.1f}% ; "
        f"Зелень: {greenery_delta:+.1f}%"
    )


def ranking(routes: List[Dict[str, object]], weights: Dict[str, float]) -> List[Dict[str, object]]:
    ranked = []
    for route in routes:
        route["comfort_score"] = comfort_score(route, weights)
        ranked.append(route)
    return sorted(ranked, key=lambda item: item["comfort_score"])
