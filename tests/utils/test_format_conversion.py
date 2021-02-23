"""Tests for format_conversion module."""
import pandas as pd
import pytest

from bwaw.utils.format_conversion import (convert_response_list_to_dataframe,
                                          convert_dataframe_to_response_list,
                                          column_str_to_datetime)

RESPONSE_LIST = [{'a': 1, 'b': 1}, {'a': 2, 'b': 2}]
RESPONSE_PANDAS = pd.DataFrame([[1, 1], [2, 2]], columns=['a', 'b'])
SERIES_TIME_ONLY = pd.Series(['12:30:00'])
TIME = pd.Timestamp("1900-01-01 12:30:00")
SERIES_FULL = pd.Series(['2021-02-21 12:30:00'])
FULL = pd.Timestamp('2021-02-21 12:30:00')


def test_convert_response_list_to_dataframe():
    """Test for bwaw.utils.format_conversion.convert_response_list_to_dataframe"""
    assert convert_response_list_to_dataframe(RESPONSE_LIST).equals(RESPONSE_PANDAS)

    with pytest.raises(TypeError):
        convert_response_list_to_dataframe(pd.DataFrame([1, 2, 3]))
        convert_response_list_to_dataframe(5)
        convert_response_list_to_dataframe('abc')


def test_convert_dataframe_to_response_list():
    """Test for bwaw.utils.format_conversion.convert_dataframe_to_response_list"""
    assert convert_dataframe_to_response_list(RESPONSE_PANDAS) == RESPONSE_LIST

    with pytest.raises(TypeError):
        convert_dataframe_to_response_list([1, 2, 3])
        convert_dataframe_to_response_list(5)
        convert_dataframe_to_response_list('abc')


def test_column_str_to_datetime():
    """Test for bwaw.utils.format_conversion.column_str_to_datetime"""
    with pytest.raises(TypeError):
        column_str_to_datetime([1, 2, 3])
        column_str_to_datetime(pd.Series(['24-2-05']))
        column_str_to_datetime(pd.Series(['24-15-12 12.12.12']))

    assert column_str_to_datetime(SERIES_TIME_ONLY, time_only=True)[0] == TIME
    assert column_str_to_datetime(SERIES_FULL)[0] == FULL
