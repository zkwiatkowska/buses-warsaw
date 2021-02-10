"""Data processing utils for data analysis."""
from typing import Union
import pandas as pd
from bwaw.utils.validation import (validate_matches_time_format, validate_if_contains_columns,
                                   validate_data_is_time_column, validate_data_is_type,
                                   validate_multiple_params)


def _get_all_of_value(data: pd.DataFrame, name: str, value: Union[str, int, float]) -> pd.DataFrame:
    validate_data_is_type(data, pd.DataFrame)
    validate_if_contains_columns(data, [name])
    return data[data[name] == value].reset_index(drop=True)


def _adjust_date(column: pd.Series, start_from: pd.Timestamp):
    validate_data_is_type(column, pd.Series)
    validate_data_is_time_column(column)

    pre_start = column[column.dt.time < start_from.time()]
    post_start = column[column.dt.time >= start_from.time()]

    post_start = pd.to_datetime(post_start.apply(lambda x: f'{start_from.date()} {x.time()}'))
    day_after = start_from.date() + pd.Timedelta(days=1)
    pre_start = pd.to_datetime(pre_start.apply(lambda x: f'{day_after} {x.time()}'))

    output = pd.concat((pre_start, post_start))
    assert output.shape == column.shape

    return output


def get_all_of_time(data: pd.DataFrame,
                    start: Union[str, pd.Timestamp],
                    end: Union[str, pd.Timestamp],
                    time_name: str = 'Time') -> pd.DataFrame:
    """
    Restrict data to dates between start and end.
    Args:
        data: data containing time column for conditioning
        start: start time
        end: end time
        time_name: name of column containing time

    Returns:
        restricted dataset.
    """
    if not (isinstance(start, pd.Timestamp) or isinstance(end, pd.Timestamp)):
        validate_multiple_params([start, end], lambda x: validate_data_is_type(x, str))
        validate_matches_time_format(start)
        validate_matches_time_format(end)
        start, end = pd.Timestamp(start), pd.Timestamp(end)

    validate_data_is_type(data, pd.DataFrame)
    validate_data_is_time_column(data[time_name])

    return data[(start <= data[time_name]) & (data[time_name] <= end)].reset_index(drop=True)


def get_all_of_line(data: pd.DataFrame, line: str) -> pd.DataFrame:
    """
    Restrict data to chosen line.
    Args:
        data: data containing line column for conditioning
        line: chosen line

    Returns:
        restricted dataset.
    """
    return _get_all_of_value(data=data, name='Lines', value=line).reset_index(drop=True)


def get_all_of_brigade(data: pd.DataFrame, brigade: Union[str, int]) -> pd.DataFrame:
    """
    Restrict data to chosen brigade.
    Args:
        data: data containing line column for conditioning
        brigade: chosen line

    Returns:
        restricted dataset.
    """
    return _get_all_of_value(data=data, name='Brigade', value=brigade).reset_index(drop=True)


def remove_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicates from data and reset index.
    Args:
        data: any data frame

    Returns:
        restricted dataset.
    """
    validate_data_is_type(data, pd.DataFrame)
    return data.drop_duplicates().reset_index(drop=True)
