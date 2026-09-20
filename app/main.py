from __future__ import annotations

from datetime import date as Date, time as Time

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.routing.route_optimizer import DEFAULT_WEIGHTS, build_demo_routes

app = FastAPI(
    title="Bishkek Comfort Map",
    description="Comfort-aware pedestrian routing prototype for Bishkek.",
    version="0.1.0",
)


class RouteRequest(BaseModel):
    """Validated input for route calculation."""

    model_config = ConfigDict(str_strip_whitespace=True)

    origin: str = Field(default="A", min_length=1, max_length=100)
    destination: str = Field(default="B", min_length=1, max_length=100)
    date: Date = Date(2026, 6, 15)
    time: Time = Time(8, 30)
    sun_weight: float = Field(default=DEFAULT_WEIGHTS["sun"], ge=0, le=10)
    greenery_weight: float = Field(default=DEFAULT_WEIGHTS["greenery"], ge=0, le=10)
    sidewalk_weight: float = Field(default=DEFAULT_WEIGHTS["sidewalk"], ge=0, le=10)
    stairs_weight: float = Field(default=DEFAULT_WEIGHTS["stairs"], ge=0, le=10)
    speed_weight: float = Field(default=DEFAULT_WEIGHTS["speed"], ge=0, le=10)

    @field_validator("origin", "destination")
    @classmethod
    def reject_blank_location(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("location must not be blank")
        return value


@app.get("/")
def root() -> dict[str, object]:
    return {
        "project": "Bishkek Comfort Map",
        "status": "prototype",
        "mvp": "0.1",
        "description": "Comfort-aware pedestrian routing for Bishkek",
        "routes": ["fast", "shaded", "comfortable"],
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/routes")
def get_routes(payload: RouteRequest) -> dict[str, object]:
    weights = {
        "sun": payload.sun_weight,
        "greenery": payload.greenery_weight,
        "sidewalk": payload.sidewalk_weight,
        "stairs": payload.stairs_weight,
        "speed": payload.speed_weight,
    }
    alternatives = build_demo_routes(
        origin=payload.origin,
        destination=payload.destination,
        date=payload.date.isoformat(),
        time=payload.time.strftime("%H:%M"),
        weights=weights,
    )

    return {
        "origin": payload.origin,
        "destination": payload.destination,
        "date": payload.date.isoformat(),
        "time": payload.time.strftime("%H:%M"),
        "alternatives": alternatives,
    }
