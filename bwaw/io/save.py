"""Saving utils."""
import pickle
from pathlib import Path
from typing import List, Union
import pandas as pd
from bwaw.utils.format_conversion import convert_response_list_to_dataframe
from bwaw.utils.validation import validate_data_is_type


def _validate_save_parameters(data: Union[List, pd.DataFrame], path: Union[Path, str],
                              suffix: str) -> None:
    """
    Validates typical parameters for save function in bwaw library.
    Args:
        data: data to be saved
        path: path where to store data
        suffix: target path suffix
    """
    validate_data_is_type(path, (Path, str))
    validate_data_is_type(data, (list, pd.DataFrame))
    if not str(path).endswith(suffix):
        raise ValueError(f'Path must have {suffix} suffix.')


def save_response_to_csv(data: Union[List, pd.DataFrame], path: Union[Path, str]) -> None:
    """
    Save response list to .csv file.
    Args:
        data: data in the format of response list (values or dicts)
        path: path where to store data
    """
    _validate_save_parameters(data, path, '.csv')
    if isinstance(data, list):
        data = convert_response_list_to_dataframe(data)
    path = Path(path) if isinstance(path, str) else path
    path.parent.mkdir(exist_ok=True, parents=True)
    data.to_csv(path, index=False)


def save_response_to_pickle(data: Union[List, pd.DataFrame], path: Union[Path, str]) -> None:
    """
    Save response list to .pkl file.
    Args:
        data: data in the format of response list (values or dicts)
        path: path where to store data
    """
    _validate_save_parameters(data, path, '.pkl')
    path = Path(path) if isinstance(path, str) else path
    path.parent.mkdir(exist_ok=True, parents=True)
    with path.open('wb') as output_file:
        pickle.dump(data, output_file)
