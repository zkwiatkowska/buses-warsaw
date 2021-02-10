"""Speed insights extraction."""
from typing import Tuple

import pandas as pd
import numpy as np

from bwaw.insights.math_ops import (_calculate_distance_km, _calculate_time_difference_hours,
                                    _calculate_speed)
from bwaw.utils.validation import validate_if_contains_columns, validate_data_is_type
from bwaw.insights.data import get_all_of_line, get_all_of_brigade


def _report_incident(subset: pd.DataFrame, speed: float) -> dict:
    return {
        'Speed': speed,
        'Lat': subset['Lat'].mean(),
        'Lon': subset['Lon'].mean(),
        'Time': subset['Time'].mean()
    }


def _create_grid(min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> Tuple:
    latitude = np.linspace(start=min_lat, stop=max_lat, num=9)
    longitude = np.linspace(start=min_lon, stop=max_lon, num=9)
    return latitude, longitude


def _value_to_grid_index(value: float, grid: np.ndarray) -> np.ndarray:
    arg = np.argmax([value <= i for i in grid[1:]])
    return arg


def _grid_index_to_center_value(grid_idx: np.ndarray, grid: np.ndarray) -> float:
    return (grid[grid_idx + 1] + grid[grid_idx]) / 2


def _find_grid(column: pd.Series, grid: np.ndarray) -> pd.Series:
    column = column.apply(lambda x: _value_to_grid_index(x, grid))
    return column


def get_speed_incidents_for_bus(data: pd.DataFrame, speed_limit: int) -> pd.DataFrame:
    """
    Get all speed incidents for a single bus.
    Args:
        data: data regarding bus activity
        speed_limit: maximum speed limit we treat as acceptable (km/hour).

    Returns:
        All speed incidents in the format based on _report_incident
    """
    validate_if_contains_columns(data, ['Lon', 'Lat', 'Time', 'Lines', 'Brigade'])
    validate_data_is_type(speed_limit, int)
    if len(data['Lines'].unique()) > 1 or len(data['Brigade'].unique()) > 1:
        raise ValueError('Data does not consist of information from single bus/brigade.')

    data.sort_values(by='Time', ascending=True, inplace=True)
    data.reset_index(drop=True, inplace=True)
    report = []

    for i in range(len(data) - 1):
        distance = _calculate_distance_km(lon_x=data.at[i, 'Lon'], lat_x=data.at[i, 'Lat'],
                                          lon_y=data.at[i+1, 'Lon'], lat_y=data.at[i+1, 'Lat'])
        time = _calculate_time_difference_hours(data.at[i, 'Time'], data.at[i+1, 'Time'])
        if time:
            speed = _calculate_speed(distance, time)

            if 150 > speed > speed_limit:
                report.append(_report_incident(data.iloc[[i, i+1]], speed))

    return pd.DataFrame(report)


def get_all_incidents(data: pd.DataFrame, speed_limit: int) -> pd.DataFrame:
    """
    Get all speed incidents for all buses.
    Args:
        data: data regarding all buses activity
        speed_limit: maximum speed limit we treat as acceptable (km/hour).

    Returns:
        All speed incidents in the format based on _report_incident
    """
    validate_if_contains_columns(data, ['Lines', 'Brigade', 'Lon', 'Lat', 'Time'])
    validate_data_is_type(speed_limit, int)
    data.sort_values(by='Time', ascending=True, inplace=True)
    data.reset_index(drop=True, inplace=True)
    report = pd.DataFrame(columns=['Lines', 'Speed', 'Lat', 'Lon', 'Time'])

    for line in data['Lines'].unique():
        per_line = get_all_of_line(data, line)
        for brigade in per_line['Brigade'].unique():
            per_brigade = get_all_of_brigade(per_line, brigade)
            incidents = get_speed_incidents_for_bus(per_brigade, speed_limit)
            if len(incidents) > 0:
                incidents['Lines'] = line
                report = report.append(incidents)

    return report.reset_index(drop=True)


def get_short_incidents_summary(data: pd.DataFrame, speed_limit: int) -> Tuple[str, pd.DataFrame]:
    """
    Get all incidents summary (total number, bus incidents ratio).
    Args:
        data: data regarding all buses activity
        speed_limit: maximum speed limit we treat as acceptable (km/hour).

    Returns:
        Human readable incidents short summary.
    """

    report = get_all_incidents(data, speed_limit)
    summary = f'Speed limit: {speed_limit} km/h.\n'
    summary += f'Total number of incidents: {len(report)}.\n'

    buses_with_incidents = len(report["Lines"].unique())
    total_buses = len(data["Lines"].unique())
    ratio = round(100 * buses_with_incidents / total_buses, 2)

    summary += f'{buses_with_incidents}/{total_buses} buses had incidents ({ratio}%).\n'

    return summary, report


def get_full_incidents_summary(data: pd.DataFrame, speed_limit: int) -> Tuple[str, pd.DataFrame]:
    """
    Get all incidents summary (short + top buses, top places).
    Args:
        data: data regarding all buses activity
        speed_limit: maximum speed limit we treat as acceptable (km/hour).

    Returns:
        Human readable incidents long summary.
    """
    summary, report = get_short_incidents_summary(data, speed_limit)
    summary += 'Top 3 buses with highest number of incidents were:\n'

    top_3 = report["Lines"].value_counts().sort_values(ascending=False).head(3)
    top_3 = top_3.apply(lambda x: f'{x} incidents')
    summary += top_3.to_string() + '\n'

    report = report.groupby(by='Lines')[['Lat', 'Lon']].mean()

    lat_grid, lon_grid = _create_grid(min_lat=report['Lat'].min(), max_lat=report['Lat'].max(),
                                      min_lon=report['Lon'].min(), max_lon=report['Lon'].max())

    report['Lat_grid'] = _find_grid(report['Lat'], lat_grid)
    report['Lon_grid'] = _find_grid(report['Lon'], lon_grid)

    top_3 = report.groupby(by=['Lat_grid', 'Lon_grid']).count()\
        .sort_values(by='Lat', ascending=False).head(3)
    summary += 'Top 3 places with highest number of incidents were:\n'
    for (i, j), buses_count in top_3.iterrows():
        lat = round(_grid_index_to_center_value(i, lat_grid), 2)
        lon = round(_grid_index_to_center_value(j, lon_grid), 2)
        summary += f'({lat}, {lon}) - {buses_count["Lat"]} incidents.\n'

    return summary, report
