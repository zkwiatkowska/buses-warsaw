"""Formatting information from UM Warszawa API (UMWaw API) responses."""
from typing import List
from bwaw.utils.validation import validate_matches_time_format


def _correct_time(time: str) -> str:
    """
    Corrects time from timetable response (hour higher than 23).
    Args:
        time: time from timetable response

    Returns:
        corrected time
    """
    validate_matches_time_format(time)
    split_time = time.split(':')
    if int(split_time[0]) >= 24:
        new_hour = int(split_time[0]) % 24
        if new_hour < 10:
            split_time[0] = f'0{new_hour}'
        else:
            split_time[0] = str(new_hour)
    return ':'.join(split_time)


def _format_simple_key_value_response(response: dict,
                                      information_key: str,
                                      error_msg_parameter: str) -> List:
    """
    Formats most basic types of responses by extracting list of target information.
    Args:
        response: response from UMWaw API
        information_key: key pointing out to target information
        error_msg_parameter: name of request parameter in case of error

    Returns:
        list of target information
    """
    response = response['result']
    if len(response) > 0:
        response = [item['value'] for values in response for item in values['values']
                    if item['key'] == information_key]
        return response

    raise ValueError(f'Incorrect {error_msg_parameter}. No results found.')


def _format_active_bus_response(response: dict) -> List:
    """
    Formats response with currently active buses.
    Args:
        response: not processed response with currently active buses.

    Returns:
        list of dicts with active buses data.
    """
    return response['result']


def _format_bus_stop_id_response(response: dict) -> List:
    """
    Formats response with all bus stop ids for bus stop name.
    Args:
        response: not processed response with all bus stop ids for bus stop name.

    Returns:
        list of ids
    """
    return _format_simple_key_value_response(response=response,
                                             information_key='zespol',
                                             error_msg_parameter='bus stop name')


def _format_all_lines_on_stop_response(response: dict) -> List:
    """
    Formats response with all lines on bus stop.
    Args:
        response: not processed response with all lines on bus stop.

    Returns:
        list of lines on bus stop
    """
    return _format_simple_key_value_response(response=response,
                                             information_key='linia',
                                             error_msg_parameter='bus stop number')


def _format_all_coordinates_response(response: dict) -> List:
    """
    Formats response with all coordinates.
    Args:
        response: not processed response with all coordinates.

    Returns:
        list of coordinates
    """
    response = response['result']
    if len(response) > 0:
        keys = ['zespol', 'slupek', 'szer_geo', 'dlug_geo', 'kierunek', 'obowiazuje_od']
        new_names = ['ID', 'Number', 'Latitude', 'Longitude', 'Destination', 'Validity']
        response = [[d['value'] for d in item['values'] if d['key'] in keys] for item in response]
        response = [dict(zip(new_names, i)) for i in response]
        return response

    raise ValueError('No results found.')


def _format_timetable_on_stop_response(response: dict) -> List:
    """
    Formats response with timetable of line on bus stop.
    Args:
        response: not processed response with timetable of line on bus stop.

    Returns:
        list of dicts containing timetable metadata
    """
    response = response['result']
    if len(response) > 0:
        keys = ['brygada', 'kierunek', 'czas']
        response = [[d['value'] for d in item['values'] if d['key'] in keys] for item in response]
        response = [dict(zip(['Brigade', 'Destination', 'Time'], i)) for i in response]
        for item in response:
            item['Time'] = _correct_time(item['Time'])
        return response

    raise ValueError('Incorrect bus stop or line number. No results found.')
