from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Node:
    id: str
    x: float
    y: float
    elevation: float = 0.0


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    distance_m: float
    walking_time_min: float
    sun_exposure: float = 0.0
    shade_ratio: float = 0.0
    greenery: float = 0.0
    sidewalk_quality: float = 0.0
    stairs: float = 0.0
    crossings: float = 0.0
    transport_access: float = 0.0


@dataclass
class RouteAlternative:
    name: str
    nodes: list[str]
    total_distance_km: float
    total_time_min: float
    average_shade: float
    greenery: float
    sidewalk_quality: float
    stairs: float = 0.0
    crossings: float = 0.0
    explanation: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "nodes": list(self.nodes),
            "total_distance_km": round(self.total_distance_km, 2),
            "total_time_min": round(self.total_time_min, 1),
            "average_shade": round(self.average_shade, 2),
            "greenery": round(self.greenery, 2),
            "sidewalk_quality": round(self.sidewalk_quality, 2),
            "stairs": round(self.stairs, 2),
            "crossings": round(self.crossings, 2),
            "explanation": list(self.explanation),
        }
