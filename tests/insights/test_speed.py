"""Tests for speed module."""
import pytest
import pandas as pd
import numpy as np
from bwaw.insights.speed import (get_speed_incidents_for_bus, get_all_incidents,
                                 get_short_incidents_summary, get_full_incidents_summary)
from tests.insights import ACTIVE_BUSES, SPEED_INCIDENT, SPEED_INCIDENTS


def test_get_speed_incidents_for_bus():
    """Test for bwaw.insights.speed.get_speed_incidents_for_bus"""
    with pytest.raises(TypeError):
        get_speed_incidents_for_bus(pd.DataFrame(columns=['Lon', 'Lat', 'Time', 'Lines']), 50.4)

    with pytest.raises(ValueError):
        get_speed_incidents_for_bus(pd.DataFrame(), 50)
        get_speed_incidents_for_bus(ACTIVE_BUSES, 50)

    output = get_speed_incidents_for_bus(ACTIVE_BUSES[ACTIVE_BUSES['Lines'] == '138'], 10)
    for col in output.columns:
        if col != 'Time':
            assert np.allclose(output[col], SPEED_INCIDENT[col])
        else:
            assert np.all(output[col] == SPEED_INCIDENT[col])


def test_get_all_incidents():
    """Test for bwaw.insights.speed.get_all_incidents"""
    with pytest.raises(TypeError):
        get_all_incidents(pd.DataFrame(columns=['Lines', 'Brigade', 'Lon', 'Lat', 'Time']), 50.4)

    with pytest.raises(ValueError):
        get_all_incidents(pd.DataFrame(), 50)

    output = get_all_incidents(ACTIVE_BUSES, 10)
    for col in output.columns:
        if col not in ['Time', 'Lines']:
            assert np.allclose(output[col], SPEED_INCIDENTS[col])
        else:
            assert np.all(output[col] == SPEED_INCIDENTS[col])


def test_get_short_incidents_summary():
    """Test for bwaw.insights.speed.get_short_incidents_summary"""
    with pytest.raises(TypeError):
        get_short_incidents_summary(pd.DataFrame(columns=['Lines', 'Brigade', 'Lon',
                                                          'Lat', 'Time']), 50.4)

    with pytest.raises(ValueError):
        get_short_incidents_summary(pd.DataFrame(), 50)

    output = 'Speed limit: 10 km/h.\nTotal number of incidents: 2.\n' \
             '2/2 buses had incidents (100.0%).\n'
    assert output == get_short_incidents_summary(ACTIVE_BUSES, 10)[0]


def test_get_full_incidents_summary():
    """Test for bwaw.insights.speed.get_full_incidents_summary"""
    with pytest.raises(TypeError):
        get_full_incidents_summary(pd.DataFrame(columns=['Lines', 'Brigade', 'Lon',
                                                         'Lat', 'Time']), 50.4)

    with pytest.raises(ValueError):
        get_full_incidents_summary(pd.DataFrame(), 50)

    output = 'Speed limit: 10 km/h.\nTotal number of incidents: 2.\n' \
             '2/2 buses had incidents (100.0%).\n'
    output += 'Top 3 buses with highest number of incidents were:\n213    1 incidents' \
              '\n138    1 incidents\n'
    output += 'Top 3 places with highest number of incidents were:\n(52.22, 21.09) - 2 incidents.\n'

    assert output == get_full_incidents_summary(ACTIVE_BUSES, 10)[0]
