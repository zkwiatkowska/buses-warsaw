"""Tests for load module."""
from pathlib import Path
import pytest
import pandas as pd
from bwaw.io.load import load_response_from_pickle, load_response_from_csv

ANSWER = pd.DataFrame([{
    'ID': '1001',
    'Number': '01',
    'Latitude': '52.248455',
    'Longitude': '21.044827',
    'Destination': 'al.Zieleniecka',
    'Validity': '2020-10-12 00:00:00.0'
}])

resources_path = Path.cwd() / 'tests' if Path.cwd().name != 'tests' else Path.cwd()


def test_load_response_from_csv():
    """Test for bwaw.io.load.load_response_from_csv"""
    with pytest.raises(TypeError):
        load_response_from_csv(5)

    loaded = load_response_from_csv(resources_path / 'resources/test.csv')
    assert loaded.equals(ANSWER)


def test_load_response_from_pickle():
    """Test for bwaw.io.load.load_response_from_pickle"""
    with pytest.raises(TypeError):
        load_response_from_pickle(5)

    loaded = load_response_from_pickle(resources_path / 'resources/test.pkl')
    assert loaded.equals(ANSWER)
