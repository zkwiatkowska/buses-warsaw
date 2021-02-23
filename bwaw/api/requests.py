"""Highest level module to get data from UM Warszawa API (UMWaw API)."""

from typing import List
from urllib import request, parse
from bwaw.api import CONSTANTS, TABLE, RESOURCE_ID, PARAMETER
from bwaw.api.download import _get_resource_from_request, _get_resource_over_time
from bwaw.api.formatting import (_format_bus_stop_id_response, _format_all_lines_on_stop_response,
                                 _format_timetable_on_stop_response, _format_active_bus_response,
                                 _format_all_coordinates_response)
from bwaw.utils.validation import validate_data_is_type, validate_multiple_params


def _create_request(table_name: str,
                    parameters: dict) -> request.Request:
    """
    Creates an arbitrary request conforming to API guidelines.
    Args:
        table_name: name of the table in UMWaw database
        parameters: parameters related to request

    Returns:
        GET request for UMWaw API
    """
    return request.Request(f"{CONSTANTS.API_URL}{table_name}/?{parse.urlencode(parameters)}")


def _create_active_buses_request(api_key: str) -> request.Request:
    """
    Creates a request for list of active buses.
    Args:
        api_key: API key provided by UMWaw

    Returns:
        request for list of active buses
    """
    validate_data_is_type(api_key, str)
    return _create_request(table_name=TABLE.BUSES, parameters={
        PARAMETER.RESOURCE_ID1: RESOURCE_ID.BUSES_ACTIVE,
        PARAMETER.API_KEY: api_key,
        PARAMETER.TYPE: CONSTANTS.ACTIVE_BUS_STATIC_TYPE

    })


def get_active_buses(api_key: str) -> List:
    """
    Get method for list of all currently active buses.
    Args:
        api_key: API key provided by UMWaw

    Returns:
        list of metadata of all currently active buses
    """
    validate_data_is_type(api_key, str)
    response = _get_resource_from_request(resource_request=_create_active_buses_request(api_key))
    return _format_active_bus_response(response)


def get_active_buses_over_time(api_key: str,
                               no_of_requests: int = 1,
                               interval_btwn_requests: int = 1,
                               keep_partial_if_fail: bool = True) -> List:
    """
    Get method for list of all currently active buses requested over some period.
    Args:
        api_key: API key provided by UMWaw
        no_of_requests: number of calls to UMWaw
        interval_btwn_requests: time [minutes] between calls to UMWaw
        keep_partial_if_fail: if partial results should be stored if call fails

    Returns:
        list of metadata of all currently active buses aggregated from whole period
    """
    validate_data_is_type(api_key, str)
    response = _get_resource_over_time(resource_request=_create_active_buses_request(api_key),
                                       no_of_requests=no_of_requests,
                                       interval_btwn_requests=interval_btwn_requests,
                                       keep_partial_if_fail=keep_partial_if_fail)
    return [d for r in response for d in _format_active_bus_response(r)]


def get_bus_stops_ids_by_name(api_key: str,
                              name: str) -> List:
    """
    Get method for list of all bus stops' ids by bus stop name.
    Args:
        api_key: API key provided by UMWaw
        name: bus stop name

    Returns:
        list of all bus stops' ids by bus stop name
    """
    validate_multiple_params([api_key, name], lambda x: validate_data_is_type(x, str))
    req = _create_request(table_name=TABLE.TIMETABLES, parameters={
        PARAMETER.RESOURCE_ID2: RESOURCE_ID.BUS_STOP_BY_NAME,
        PARAMETER.API_KEY: api_key,
        PARAMETER.BUS_STOP_NAME: name

    })
    response = _get_resource_from_request(resource_request=req)
    return _format_bus_stop_id_response(response)


def get_all_lines_on_bus_stop(api_key: str,
                              bus_stop_id: str,
                              bus_stop_nr: str) -> List:
    """
    Get method for list of all bus lines on given bus stop.
    Args:
        api_key: API key provided by UMWaw
        bus_stop_id: bus stop identifier
        bus_stop_nr: bus stop number (eg. 01, 02, etc.)

    Returns:
        list of all bus lines on given bus stop
    """
    validate_multiple_params([api_key, bus_stop_nr, bus_stop_id],
                             lambda x: validate_data_is_type(x, str))
    req = _create_request(table_name=TABLE.TIMETABLES, parameters={
        PARAMETER.RESOURCE_ID2: RESOURCE_ID.BUSES_ON_STOP,
        PARAMETER.API_KEY: api_key,
        PARAMETER.BUS_STOP_ID: bus_stop_id,
        PARAMETER.BUS_STOP_NR: bus_stop_nr

    })
    response = _get_resource_from_request(resource_request=req)
    return _format_all_lines_on_stop_response(response)


def get_timetable_for_line_on_bus_stop(api_key: str,
                                       bus_stop_id: str,
                                       bus_stop_nr: str,
                                       line: str) -> List:
    """
    Get method for list of line timetable on bus stop.
    Args:
        api_key: API key provided by UMWaw
        bus_stop_id: bus stop identifier
        bus_stop_nr: bus stop number (eg. 01, 02, etc.)
        line: bus line number

    Returns:
        list of line timetable on bus stop.
    """
    validate_multiple_params([api_key, bus_stop_id, bus_stop_nr, line],
                             lambda x: validate_data_is_type(x, str))

    req = _create_request(table_name=TABLE.TIMETABLES, parameters={
        PARAMETER.RESOURCE_ID2: RESOURCE_ID.TIMETABLE_FOR_LINE,
        PARAMETER.API_KEY: api_key,
        PARAMETER.BUS_STOP_ID: bus_stop_id,
        PARAMETER.BUS_STOP_NR: bus_stop_nr,
        PARAMETER.LINE_NR: line

    })
    response = _get_resource_from_request(resource_request=req)
    return _format_timetable_on_stop_response(response)


def get_bus_stops_coordinates(api_key: str) -> List:
    """
    Get method for list of all bus stops' coordinates.
    Args:
        api_key: API key provided by UMWaw

    Returns:
        list of all bus stops' coordinates
    """
    validate_data_is_type(api_key, str)
    req = _create_request(table_name=TABLE.STOPS, parameters={
        PARAMETER.RESOURCE_ID2: RESOURCE_ID.BUS_STOP_COORDINATE,
        PARAMETER.API_KEY: api_key

    })
    response = _get_resource_from_request(resource_request=req)
    return _format_all_coordinates_response(response)
