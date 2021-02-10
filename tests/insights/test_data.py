"""Tests for data module."""
import pandas as pd
import numpy as np
import pytest

from bwaw.insights.data import (get_all_of_line, get_all_of_time,
                                get_all_of_brigade, remove_duplicates)


def _test_numericals(proper_col_name, wrong_col_name, value, func):
    proper_input = pd.DataFrame(['123', '138'], columns=[proper_col_name])
    wrong_input_column = pd.DataFrame(['123', '138'], columns=[wrong_col_name])
    wrong_input_format = [1, 2, 3]

    with pytest.raises(TypeError):
        func(wrong_input_format, '123')

    with pytest.raises(ValueError):
        func(wrong_input_column, '123')

    assert func(proper_input, value).equals(pd.DataFrame([value], columns=[proper_col_name]))


def test_get_all_of_time():
    """Test for bwaw.insights.data.get_all_of_time"""
    all_dates = np.array(['2021-02-01 12:30:00',
                          '2021-02-01 13:30:00',
                          '2021-02-01 14:30:00']).astype('datetime64[ns]')
    proper_input = pd.DataFrame(all_dates, columns=['Time'])
    wrong_col_format = pd.DataFrame([1, 2, 3], columns=['Time'])
    wrong_format = [1, 2, 3]

    str_start_ok, str_end_ok = '2021-02-01 12:15:00', '2021-02-01 13:15:00'
    ok_output = pd.DataFrame(np.array(['2021-02-01 12:30:00']).astype('datetime64[ns]'),
                             columns=['Time'])

    str_start_wrong = '2021-02-01 12.15.00'

    pd_start_ok, pd_end_ok = pd.Timestamp(str_start_ok), pd.Timestamp(str_end_ok)

    with pytest.raises(TypeError):
        get_all_of_time(data=proper_input, start=5, end=5)
        get_all_of_time(data=wrong_col_format, start=str_start_ok, end=str_end_ok)
        get_all_of_time(data=wrong_format, start=str_start_ok, end=str_end_ok)

    with pytest.raises(ValueError):
        get_all_of_time(data=proper_input, start=str_start_wrong, end=str_end_ok)

    assert get_all_of_time(data=proper_input, start=str_start_ok, end=str_end_ok).equals(ok_output)
    assert get_all_of_time(data=proper_input, start=pd_start_ok, end=pd_end_ok).equals(ok_output)


def test_get_all_of_line():
    """Test for bwaw.insights.data.get_all_of_line"""
    _test_numericals('Lines', 'Li', '123', get_all_of_line)


def test_get_all_of_brigade():
    """Test for bwaw.insights.data.get_all_of_brigade"""
    _test_numericals('Brigade', 'Brig', '123', get_all_of_brigade)


def test_remove_duplicates():
    """Test for bwaw.insights.data.remove_duplicates"""
    proper_data = pd.DataFrame([[1, 2], [1, 2], [2, 1]], columns=['a', 'b'])
    wrong_data = [1, 2, 3]

    with pytest.raises(TypeError):
        remove_duplicates(wrong_data)

    remove_duplicates(proper_data).equals(pd.DataFrame([[1, 2], [2, 1]], columns=['a', 'b']))
