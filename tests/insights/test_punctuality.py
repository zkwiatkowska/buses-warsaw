"""Tests for punctuality module."""
import pandas as pd
import pytest

from bwaw.insights.punctuality import (get_punctuality_report, get_punctuality_list_for_bus,
                                       get_punctuality_list_for_buses)
from tests.insights import ACTIVE_BUSES, COORDINATES, TIMETABLE


PROPER_API_KEY = "5fbe79ed-1f5b-4019-ab03-641443842d8b"


def _types_check(func):
    with pytest.raises(TypeError):
        func('a', pd.DataFrame(), api_key='abc', proximity=1, time=1)
        func(pd.DataFrame(), 'a', api_key='abc', proximity=1, time=1)
        func(pd.DataFrame(), pd.DataFrame(), api_key=12345, proximity=1, time=1)
        func(pd.DataFrame(), pd.DataFrame(), api_key='abc', proximity='6', time=1)
        func(pd.DataFrame(), pd.DataFrame(), api_key='abc', proximity=1, time='5')


def test_get_punctuality_list_for_bus(mocker):
    """Test for bwaw.insights.punctuality.get_punctuality_list_for_bus"""
    _types_check(get_punctuality_list_for_bus)
    mocker.patch('bwaw.insights.punctuality._process_online', return_value=TIMETABLE)
    output = [False]
    assert get_punctuality_list_for_bus(ACTIVE_BUSES[ACTIVE_BUSES['Lines'] == '213'],
                                        COORDINATES,
                                        api_key=PROPER_API_KEY) == output


def test_get_punctuality_list_for_buses(mocker):
    """Test for bwaw.insights.punctuality.get_punctuality_list_for_buses"""
    _types_check(get_punctuality_list_for_buses)
    mocker.patch('bwaw.insights.punctuality._process_online', return_value=TIMETABLE)
    output = {'213': [False], '138': [False]}
    assert get_punctuality_list_for_buses(ACTIVE_BUSES, COORDINATES,
                                          api_key=PROPER_API_KEY) == output


def test_get_punctuality_report(mocker):
    """Test for bwaw.insights.punctuality.get_punctuality_report"""
    _types_check(get_punctuality_report)
    mocker.patch('bwaw.insights.punctuality._process_online', return_value=TIMETABLE)
    output = 'Percentage of punctuality incidents:\n' \
             '- 213 line: 0.0% incidents.\n' \
             '- 138 line: 0.0% incidents.\n'
    assert get_punctuality_report(ACTIVE_BUSES, COORDINATES, api_key=PROPER_API_KEY) == output
