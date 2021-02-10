"""Tests for request module."""
from urllib import error

import pytest

from bwaw.api.requests import (get_active_buses, get_active_buses_over_time,
                               get_bus_stops_ids_by_name, get_all_lines_on_bus_stop,
                               get_timetable_for_line_on_bus_stop, get_bus_stops_coordinates)


PROPER_API_KEY = "5fbe79ed-1f5b-4019-ab03-641443842d8b"
WRONG_API_KEY = "5fbe79ed-1111-1111-1111-641443842d8b"


def test_get_active_buses(mocker):
    """Test for bwaw.api.requests.get_active_buses"""
    with pytest.raises(error.HTTPError):
        get_active_buses(WRONG_API_KEY)
    response_list = [1, 2, 3]
    mocker.patch('bwaw.api.requests._get_resource_from_request',
                 return_value={'result': response_list})
    assert get_active_buses(PROPER_API_KEY) == [1, 2, 3]


def test_get_active_buses_over_time(mocker):
    """Test for bwaw.api.requests.get_active_buses_over_time"""
    with pytest.raises(RuntimeError):
        get_active_buses_over_time(WRONG_API_KEY, keep_partial_if_fail=False)
    response_list = [1, 2, 3]
    full_response = [{'result': response_list}, {'result': response_list}]

    mocker.patch('bwaw.api.requests._get_resource_over_time',
                 return_value=full_response)
    assert get_active_buses_over_time(PROPER_API_KEY,
                                      keep_partial_if_fail=False) == 2 * response_list


def test_get_bus_stops_ids_by_name(mocker):
    """Test for bwaw.api.requests.get_bus_stops_ids_by_name"""
    with pytest.raises(error.HTTPError):
        get_bus_stops_ids_by_name(WRONG_API_KEY, 'Rondo ONZ')

    with pytest.raises(ValueError):
        get_bus_stops_ids_by_name(PROPER_API_KEY, 'Random name')

    response = {'result': [{'values': [{'value': '7009', 'key': 'zespol'},
                                       {'value': 'Marszałkowska', 'key': 'nazwa'}]}]}
    formatted_response = ['7009']

    mocker.patch('bwaw.api.requests._get_resource_from_request', return_value=response)
    assert get_bus_stops_ids_by_name(PROPER_API_KEY, 'Marszałkowka') == formatted_response


def test_get_all_lines_on_bus_stop(mocker):
    """Test for bwaw.api.requests.get_all_lines_on_bus_stop"""
    with pytest.raises(error.HTTPError):
        get_all_lines_on_bus_stop(WRONG_API_KEY, '7009', '01')

    with pytest.raises(ValueError):
        get_all_lines_on_bus_stop(PROPER_API_KEY, '0000', '01')
        get_all_lines_on_bus_stop(PROPER_API_KEY, '7009', '53')

    response = {'result': [{'values': [{'value': '138', 'key': 'linia'}]},
                           {'values': [{'value': '143', 'key': 'linia'}]},
                           {'values': [{'value': '151', 'key': 'linia'}]}]}
    formatted_response = ['138', '143', '151']

    mocker.patch('bwaw.api.requests._get_resource_from_request', return_value=response)
    assert get_all_lines_on_bus_stop(PROPER_API_KEY, '7009', '01') == formatted_response


def test_get_timetable_for_line_on_bus_stop(mocker):
    """Test for bwaw.api.requests.get_timetable_for_line_on_bus_stop"""
    with pytest.raises(error.HTTPError):
        get_timetable_for_line_on_bus_stop(WRONG_API_KEY, '7009', '01', '138')

    with pytest.raises(ValueError):
        get_timetable_for_line_on_bus_stop(PROPER_API_KEY, '0000', '01', '138')
        get_timetable_for_line_on_bus_stop(PROPER_API_KEY, '7009', '53', '138')
        get_timetable_for_line_on_bus_stop(PROPER_API_KEY, '7009', '01', '1113')

    response = {'result': [{'values': [{'value': 'null', 'key': 'symbol_2'},
                                       {'value': 'null', 'key': 'symbol_1'},
                                       {'value': '010', 'key': 'brygada'},
                                       {'value': 'Utrata', 'key': 'kierunek'},
                                       {'value': 'TD-7UTS', 'key': 'trasa'},
                                       {'value': '04:39:00', 'key': 'czas'}]}]}
    formatted_response = [{'Brigade': '010', 'Destination': 'Utrata', 'Time': '04:39:00'}]

    mocker.patch('bwaw.api.requests._get_resource_from_request', return_value=response)
    assert get_timetable_for_line_on_bus_stop(PROPER_API_KEY,
                                              '7009', '01', '138') == formatted_response


def test_get_bus_stops_coordinates(mocker):
    """Test for bwaw.api.requests.get_bus_stops_coordinates"""
    with pytest.raises(error.HTTPError):
        get_bus_stops_coordinates(WRONG_API_KEY)

    response = {'result': [{'values': [{'value': '1001', 'key': 'zespol'},
                                       {'value': '01', 'key': 'slupek'},
                                       {'value': 'Kijowska', 'key': 'nazwa_zespolu'},
                                       {'value': '2201', 'key': 'id_ulicy'},
                                       {'value': '52.248455', 'key': 'szer_geo'},
                                       {'value': '21.044827', 'key': 'dlug_geo'},
                                       {'value': 'al.Zieleniecka', 'key': 'kierunek'},
                                       {'value': '2020-10-12 00:00:00.0',
                                        'key': 'obowiazuje_od'}]}]}

    formatted_response = [{'ID': '1001', 'Number': '01', 'Latitude': '52.248455',
                           'Longitude': '21.044827', 'Destination': 'al.Zieleniecka',
                           'Validity': '2020-10-12 00:00:00.0'}]

    mocker.patch('bwaw.api.requests._get_resource_from_request', return_value=response)
    assert get_bus_stops_coordinates(PROPER_API_KEY) == formatted_response
