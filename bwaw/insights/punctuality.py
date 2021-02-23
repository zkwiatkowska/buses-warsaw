"""Punctuality insights extraction."""
from pathlib import Path
from typing import List, Dict
import pandas as pd
from tqdm import tqdm

from bwaw.api.requests import get_timetable_for_line_on_bus_stop
from bwaw.insights.data import (get_all_of_line, get_all_of_brigade,
                                _adjust_date)
from bwaw.insights.math_ops import _proximity_to_tolerance
from bwaw.io.load import load_response_from_csv
from bwaw.utils.format_conversion import convert_response_list_to_dataframe, column_str_to_datetime
from bwaw.utils.validation import validate_data_is_type, validate_multiple_params


def _process_online(bus_stop_id: str,
                    bus_stop_nr: str,
                    bus_line: str,
                    api_key: str):
    response = get_timetable_for_line_on_bus_stop(api_key, bus_stop_id, bus_stop_nr, bus_line)
    return convert_response_list_to_dataframe(response)


def _process_from_directory(bus_stop_id: str,
                            bus_stop_nr: str,
                            bus_line: str,
                            path: Path):
    name = f'timetable_{bus_stop_id}_{bus_stop_nr}_{bus_line}.csv'
    return load_response_from_csv(path / name)


# pylint: disable=too-many-arguments
def _process_timetable(bus_stop_id: str,
                       bus_stop_nr: str,
                       bus_line: str,
                       brigade: str,
                       start_time_adjust: pd. Timestamp,
                       api_key: str = None,
                       path: Path = None):
    if not (api_key or path):
        raise ValueError

    if api_key:
        timetable = _process_online(bus_stop_id, bus_stop_nr, bus_line, api_key)
    else:
        timetable = _process_from_directory(bus_stop_id, bus_stop_nr, bus_line, path)

    timetable['Brigade'] = timetable['Brigade'].astype(str)
    timetable = timetable[timetable['Brigade'] == brigade]
    timetable['Time'] = column_str_to_datetime(timetable['Time'], time_only=True)
    timetable['Time'] = _adjust_date(timetable['Time'], start_from=start_time_adjust)
    return timetable


def get_punctuality_list_for_bus(bus_coordinates: pd.DataFrame,
                                 stops_coordinates: pd.DataFrame,
                                 api_key: str = None,
                                 path: Path = None,
                                 proximity: int = 10,
                                 time: int = 1,
                                 verbosity: bool = False) -> List:
    """
    Generate punctuality record for single bus.
    Args:
        bus_coordinates: array of active buses for single bus
        stops_coordinates: array of bus stops coordinates
        api_key: UMWaw API key if timetables are processed online
        path: path to directory containing .csv files if timetables are already downloaded
        proximity: proximity error regarding closeness between bus and a bus stop (in meters)
        time: minimum time meaning punctuality incident (in minutes)
        verbosity: if progress bar of timetables processing should be shown

    Returns:
        list with True - punctuality incident, False - bus on time
    """
    validate_multiple_params([bus_coordinates, stops_coordinates],
                             lambda x: validate_data_is_type(x, pd.DataFrame))
    validate_multiple_params([proximity, time],
                             lambda x: validate_data_is_type(x, int))
    if api_key:
        validate_data_is_type(api_key, str)
    if path:
        validate_data_is_type(path, Path)
    validate_data_is_type(verbosity, bool)

    progress_bar = tqdm(total=len(bus_coordinates)) if verbosity else None
    proximity = _proximity_to_tolerance(proximity)
    time *= 60
    punctuality = []
    for brigade in bus_coordinates["Brigade"].unique():
        for _, row in get_all_of_brigade(bus_coordinates, brigade).iterrows():
            found_bus_stops = stops_coordinates[
                (abs(stops_coordinates['Latitude'] - row['Lat']) < proximity)
                & (abs(stops_coordinates['Longitude'] - row['Lon']) < proximity)
            ]

            if len(found_bus_stops) > 0:
                res = found_bus_stops[["ID", "Number"]].to_dict(orient="records")[0]
                try:
                    res = _process_timetable(bus_stop_id=res['ID'],
                                             bus_stop_nr=res['Number'],
                                             bus_line=bus_coordinates.at[0, 'Lines'],
                                             brigade=brigade,
                                             start_time_adjust=bus_coordinates['Time'].min(),
                                             api_key=api_key,
                                             path=path)
                    time_diff = (res['Time'] - row['Time']).min().total_seconds()
                    punctuality.append(time_diff >= time)
                except ValueError:
                    continue

            if progress_bar:
                progress_bar.update(1)

    return punctuality


def get_punctuality_list_for_buses(buses_coordinates: pd.DataFrame,
                                   stops_coordinates: pd.DataFrame,
                                   api_key: str = None,
                                   path: Path = None,
                                   proximity: int = 10,
                                   time: int = 1,
                                   verbosity: bool = False) -> Dict:
    """
    Generate punctuality record for all buses in a file.
    Args:
        buses_coordinates: array of active buses
        stops_coordinates: array of bus stops coordinates
        api_key: UMWaw API key if timetables are processed online
        path: path to directory containing .csv files if timetables are already downloaded
        proximity: proximity error regarding closeness between bus and a bus stop (in meters)
        time: minimum time meaning punctuality incident
        verbosity: if progress bar of timetables processing should be shown

    Returns:
        dict, for each bus it is list with True - punctuality incident, False - bus on time
    """
    punctuality_data = {}
    for bus_nr in buses_coordinates['Lines'].unique():
        subset = get_all_of_line(buses_coordinates, bus_nr)
        punctuality_data[bus_nr] = get_punctuality_list_for_bus(bus_coordinates=subset,
                                                                stops_coordinates=stops_coordinates,
                                                                api_key=api_key,
                                                                path=path,
                                                                proximity=proximity,
                                                                time=time,
                                                                verbosity=verbosity)

    return punctuality_data


def get_punctuality_report(buses_coordinates: pd.DataFrame,
                           stops_coordinates: pd.DataFrame,
                           api_key: str = None,
                           path: Path = None,
                           proximity: int = 10,
                           time: int = 1,
                           verbosity: bool = False) -> str:
    """
    Generate punctuality summary for all buses in a file.
    Args:
        buses_coordinates: array of active buses
        stops_coordinates: array of bus stops coordinates
        api_key: UMWaw API key if timetables are processed online
        path: path to directory containing .csv files if timetables are already downloaded
        proximity: proximity error regarding closeness between bus and a bus stop (in meters)
        time: minimum time meaning punctuality incident
        verbosity: if progress bar of timetables processing should be shown

    Returns:
        human readable summary of punctuality insight for given active buses
    """
    report = get_punctuality_list_for_buses(buses_coordinates=buses_coordinates,
                                            stops_coordinates=stops_coordinates,
                                            api_key=api_key,
                                            path=path,
                                            proximity=proximity,
                                            time=time,
                                            verbosity=verbosity)
    report = [[k, round(100 * sum(v) / len(v), 2)] for k, v in report.items()]
    report = sorted(report, reverse=True, key=lambda x: x[1])
    summary = 'Percentage of punctuality incidents:\n'
    for i in report:
        summary += f'- {i[0]} line: {i[1]}% incidents.\n'
    return summary
# pylint: enable=too-many-arguments
