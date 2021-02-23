"""Type validators useful in responses processing."""
import re
from typing import Any, List, Type, Union, Tuple
import pandas as pd
import numpy as np


def validate_data_is_type(data: Any, dtype: Union[Type, Tuple]) -> None:
    """
    Type validator for arbitrary data and type.
    Args:
        data: arbitrary data
        dtype: arbitrary type
    """
    types = [i.__name__ for i in dtype] if isinstance(dtype, tuple) else dtype.__name__
    if not isinstance(data, dtype):
        raise TypeError(f'Data must be of type {types}.')


def validate_multiple_params(params: List[Any], validator: callable) -> None:
    """
    Wrapper for _validate_data_is_type to check multiple parameters.
    """
    for param in params:
        validator(param)


def validate_if_contains_columns(data: pd.DataFrame, columns_names: List) -> None:
    """
    Validates if pandas dataframe has columns specified.
    Args:
        data: df to verify
        columns_names: names of target columns
    """
    validate_data_is_type(data, pd.DataFrame)
    validate_data_is_type(columns_names, list)
    for column_name in columns_names:
        if column_name not in data.columns:
            raise ValueError(f"Data does not contain {column_name} column.")


def validate_data_is_time_column(data: Any) -> None:
    """
    Validates if data contains time.
    Args:
        data: arbitrary object to validate
    """
    validate_data_is_type(data, pd.Series)
    if not np.issubdtype(data, np.datetime64):
        raise TypeError('Column does not contain time.')


def validate_matches_time_format(data: str) -> None:
    """
    Validate if string is of data format accepted by bwaw
    Args:
        data: data to check
    """
    validate_data_is_type(data, str)
    date_format = '[0-9]{4}(-[0-9]{2}){2}'
    time_format = '([0-9]{2}:){2}[0-9]{2}'
    is_match = any([re.match(date_format, data),
                    re.match(time_format, data),
                    re.match(f'{date_format} {time_format}', data)])

    if not is_match:
        raise ValueError('String is not time.')
