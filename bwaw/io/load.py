"""Loading utils."""
import pickle
from pathlib import Path
from typing import Union
import pandas as pd
from bwaw.utils.format_conversion import convert_response_list_to_dataframe
from bwaw.utils.validation import validate_data_is_type


def _validate_load_parameters(path: Union[Path, str], suffix: str) -> None:
    """
    Validates typical parameters for load function in bwaw library.
    Args:
        path: path where data is stored
        suffix: target path suffix
    """
    validate_data_is_type(path, (Path, str))
    if not str(path).endswith(suffix):
        raise ValueError(f'Path must have {suffix} suffix.')


def load_response_from_csv(path: Union[Path, str]) -> pd.DataFrame:
    """
    Load response from .csv file into dataframe.
    Args:
        path: path where data is stored
    """
    _validate_load_parameters(path, '.csv')
    return pd.read_csv(path, dtype=str)


def load_response_from_pickle(path: Union[Path, str]) -> pd.DataFrame:
    """
    Load response list from .pkl file into dataframe.
    Args:
        path: path where data is stored
    """
    _validate_load_parameters(path, '.pkl')
    path = Path(path) if isinstance(path, str) else path
    with path.open('rb') as input_file:
        data = pickle.load(input_file)
    if isinstance(data, list):
        data = convert_response_list_to_dataframe(data)
    return data
