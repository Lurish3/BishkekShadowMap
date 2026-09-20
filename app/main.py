from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from src.routing.route_optimizer import build_demo_routes

app = FastAPI(
    title="Bishkek Comfort Map",
    description="Comfort-aware pedestrian routing prototype for Bishkek.",
    version="0.1.0",
)


class RouteRequest(BaseModel):
    origin: str = "A"
    destination: str = "B"
    date: str = "2026-06-15"
    time: str = "08:30"
    sun_weight: float = 1.0
    greenery_weight: float = 1.2
    sidewalk_weight: float = 1.5
    stairs_weight: float = 0.8
    speed_weight: float = 1.0


@app.get("/")
def root() -> dict:
    return {
        "project": "Bishkek Comfort Map",
        "status": "prototype",
        "mvp": "0.1",
        "description": "Comfort-aware pedestrian routing for Bishkek",
        "routes": [
            "fast",
            "shaded",
            "comfortable",
        ],
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/routes")
def get_routes(payload: RouteRequest) -> dict:
    demo_routes = build_demo_routes(
        origin=payload.origin,
        destination=payload.destination,
        date=payload.date,
        time=payload.time,
        weights={
            "sun": payload.sun_weight,
            "greenery": payload.greenery_weight,
            "sidewalk": payload.sidewalk_weight,
            "stairs": payload.stairs_weight,
            "speed": payload.speed_weight,
        },
    )

    return {
        "origin": payload.origin,
        "destination": payload.destination,
        "date": payload.date,
        "time": payload.time,
        "alternatives": demo_routes,
    }
