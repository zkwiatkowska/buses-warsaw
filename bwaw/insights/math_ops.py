"""Math operations for speed and punctuality module."""
from math import radians, cos, sin, asin, sqrt
import pandas as pd

EARTH_RADIUS_KM = 6371
PROXIMITY_APPROXIMATION_CONST = 0.00001 / 1.30578


def _calculate_distance_km(lon_x: float, lat_x: float, lon_y: float, lat_y: float) -> float:
    lon_x = radians(lon_x)
    lat_x = radians(lat_x)
    lon_y = radians(lon_y)
    lat_y = radians(lat_y)

    haversine = cos(lat_x) * cos(lat_y) * sin((lon_y - lon_x) / 2) ** 2
    haversine += sin((lat_y - lat_x) / 2) ** 2
    haversine = 2 * asin(sqrt(haversine))

    return EARTH_RADIUS_KM * haversine


def _calculate_time_difference_hours(time_x: pd.Timestamp, time_y: pd.Timestamp) -> float:
    return abs((time_y - time_x).total_seconds()) / 3600


def _calculate_speed(distance: float, time: float) -> float:
    return distance / time


def _proximity_to_tolerance(proximity: int) -> float:
    return proximity * PROXIMITY_APPROXIMATION_CONST
