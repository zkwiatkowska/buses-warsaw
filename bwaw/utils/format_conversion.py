"""Module with utilities for data types conversion."""
from typing import List
import pandas as pd
from bwaw.utils.validation import (validate_data_is_type, validate_matches_time_format)


def convert_response_list_to_dataframe(response_list: List) -> pd.DataFrame:
    """
    Converts response list to pandas data frame.
    Args:
        response_list: list of values or dicts

    Returns:
        data in the format of pandas data frame
    """
    validate_data_is_type(response_list, list)
    return pd.DataFrame(response_list)


def convert_dataframe_to_response_list(data: pd.DataFrame) -> List:
    """
    Converts pandas data frame to response list.
    Args:
        data: data in the format of pandas data frame

    Returns:
        list of values or dicts
    """
    validate_data_is_type(data, pd.DataFrame)
    if len(data.columns) == 1:
        return list(data[data.columns[0]])
    if len(data.columns) > 1:
        return [dict(row) for _, row in data.iterrows()]
    raise ValueError('Empty data frame.')


def column_str_to_datetime(column: pd.Series, time_only: bool = False) -> pd.Series:
    """
    Convert string column containing time to datetime.
    Args:
        column: given column
        time_only: if only time is provided in string

    Returns:
        formatted column
    """
    validate_data_is_type(column, pd.Series)
    for string in column:
        validate_matches_time_format(string)

    if time_only:
        return pd.to_datetime(column, format='%H:%M:%S')

    return pd.to_datetime(column)
