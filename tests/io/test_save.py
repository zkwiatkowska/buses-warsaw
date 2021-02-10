"""Tests for save module."""
from pathlib import Path
import pytest
import pandas as pd
from bwaw.io.save import save_response_to_csv, save_response_to_pickle

LIST_ANSWER = [1, 2, 3]
PANDAS_ANSWER = pd.DataFrame([[1, 2, 3]], columns=['a', 'b', 'c'])
WRONG_TYPE = 1
EXISTING_PATH = 'tests/resources/res'
NON_EXISTING_PATH = 'non/existing'


def _general_test(file_suffix, func):
    existing_path = Path(EXISTING_PATH + file_suffix)
    non_existing_path = Path(NON_EXISTING_PATH + file_suffix)

    func(LIST_ANSWER, existing_path)
    func(PANDAS_ANSWER, non_existing_path)

    with pytest.raises(TypeError):
        func(WRONG_TYPE, existing_path)

    assert existing_path.exists()
    assert non_existing_path.exists()

    existing_path.unlink()
    non_existing_path.unlink()
    non_existing_path.parent.rmdir()


def test_save_response_to_csv():
    """Test for bwaw.io.save.save_response_to_csv"""
    _general_test('.csv', save_response_to_csv)


def test_save_response_to_pickle():
    """Test for bwaw.io.save_response_to_pickle"""
    _general_test('.pkl', save_response_to_pickle)
