from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SunExposureEstimate:
    date: str
    time: str
    latitude: float
    longitude: float
    solar_angle_deg: float
    exposure_index: float
    shade_probability: float


def estimate_solar_exposure(
    date: str,
    time: str,
    latitude: float = 42.8746,
    longitude: float = 74.5698,
    building_shadow_multiplier: float = 0.52,
    tree_cover_multiplier: float = 0.28,
) -> SunExposureEstimate:
    """Simple model for MVP: not a physical measurement, only a route suitability estimate."""
    hour = int(time.split(":")[0])
    minute = int(time.split(":")[1])
    normalized_hour = (hour + minute / 60.0)

    solar_angle = 90.0 - abs(normalized_hour - 12.0) * 5.5
    solar_angle = max(5.0, min(solar_angle, 78.0))

    base_exposure = max(0.0, 100.0 - (abs(normalized_hour - 12.0) * 7.0))
    adjusted_exposure = base_exposure * (1.0 - tree_cover_multiplier)
    adjusted_exposure *= 1.0 - building_shadow_multiplier * 0.5
    adjusted_exposure = max(0.0, min(adjusted_exposure, 100.0))

    shade_probability = 1.0 - (adjusted_exposure / 100.0)
    shade_probability = max(0.0, min(shade_probability, 1.0))

    return SunExposureEstimate(
        date=date,
        time=time,
        latitude=latitude,
        longitude=longitude,
        solar_angle_deg=round(solar_angle, 2),
        exposure_index=round(adjusted_exposure, 2),
        shade_probability=round(shade_probability, 3),
    )
