from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite


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
    """Return an MVP estimate; this is not a physical solar simulation."""
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        parsed_time = datetime.strptime(time, "%H:%M").time()
    except (TypeError, ValueError) as exc:
        raise ValueError("date must be YYYY-MM-DD and time must be HH:MM") from exc

    values = (latitude, longitude, building_shadow_multiplier, tree_cover_multiplier)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("solar parameters must be finite numbers")
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise ValueError("latitude/longitude are outside valid ranges")
    if not 0.0 <= building_shadow_multiplier <= 1.0 or not 0.0 <= tree_cover_multiplier <= 1.0:
        raise ValueError("shadow multipliers must be between 0 and 1")

    hour = parsed_time.hour + parsed_time.minute / 60.0
    seasonal_factor = 1.0 + 0.08 * ((parsed_date.timetuple().tm_yday - 172) / 172)
    solar_angle = max(5.0, min(90.0 - abs(hour - 12.0) * 5.5, 78.0))
    base_exposure = max(0.0, 100.0 - abs(hour - 12.0) * 7.0) * seasonal_factor
    adjusted_exposure = base_exposure * (1.0 - tree_cover_multiplier)
    adjusted_exposure *= 1.0 - building_shadow_multiplier * 0.5
    adjusted_exposure = max(0.0, min(adjusted_exposure, 100.0))

    return SunExposureEstimate(
        date=date,
        time=time,
        latitude=latitude,
        longitude=longitude,
        solar_angle_deg=round(solar_angle, 2),
        exposure_index=round(adjusted_exposure, 2),
        shade_probability=round(max(0.0, min(1.0 - adjusted_exposure / 100.0, 1.0)), 3),
    )
