"""Tests for validation module."""
import pytest
import pandas as pd
from bwaw.utils.validation import (validate_data_is_type, validate_multiple_params,
                                   validate_if_contains_columns, validate_data_is_time_column,
                                   validate_matches_time_format)

COLUMNS_CHECK = pd.DataFrame(columns=['a', 'b', 'c'])


def test_validate_data_is_type():
    """Test for bwaw.utils.validation.validate_data_is_type"""
    with pytest.raises(TypeError):
        validate_data_is_type(5, str)
        validate_data_is_type('a', int)

    validate_data_is_type(5, int)
    validate_data_is_type(5., float)


def test_validate_multiple_params():
    """Test for bwaw.utils.validation.validate_multiple_params"""
    with pytest.raises(TypeError):
        validate_multiple_params(['a', 5], lambda x: validate_data_is_type(x, str))
        validate_multiple_params([5., 3.], lambda x: validate_data_is_type(x, int))

    validate_multiple_params([1, 2], lambda x: validate_data_is_type(x, int))
    validate_multiple_params([2., 3.], lambda x: validate_data_is_type(x, float))


def test_validate_if_contains_columns():
    """Test for bwaw.utils.validation.validate_if_contains_columns"""
    with pytest.raises(TypeError):
        validate_if_contains_columns(5, ['a'])
        validate_if_contains_columns(COLUMNS_CHECK, 'a')

    with pytest.raises(ValueError):
        validate_if_contains_columns(COLUMNS_CHECK, ['d'])

    validate_if_contains_columns(COLUMNS_CHECK, ['a'])


def test_validate_data_is_time_column():
    """Test for bwaw.utils.validation.validate_data_is_time_column"""
    with pytest.raises(TypeError):
        validate_data_is_time_column(5)
        validate_data_is_time_column(pd.Series([1, 2, 3]))

    validate_data_is_time_column(pd.Series(['2021-02-02 12:30:00'], dtype='datetime64[ns]'))


def test_validate_matches_time_format():
    """Test for bwaw.utils.validation.validate_matches_time_format"""
    validate_matches_time_format('2021-02-21')
    validate_matches_time_format('12:30:00')
    validate_matches_time_format('2021-02-21 12:30:00')

    with pytest.raises(ValueError):
        validate_matches_time_format('abcd')
        validate_matches_time_format('12.30.00')
