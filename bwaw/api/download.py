"""Module related to basic calls to UM Warszawa API (UMWaw API)."""
from pathlib import Path
from time import sleep
from typing import Dict, List, Tuple
from urllib import request, error
import logging
import json
import pickle
from tqdm import tqdm, std

PARTIAL_PATH = Path('partial.pkl')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def _store_partial_data(partial_data: List, path: Path = PARTIAL_PATH) -> None:
    """
    Stores partial data when over-time request fails.
    Args:
        partial_data: already aggregated responses
        path: where to store partial data
    """
    with path.open('wb') as file:
        pickle.dump(partial_data, file)


def _restore_partial_data(path: Path = PARTIAL_PATH) -> List:
    """
    Reads partial data from past failed request.
    Args:
        path: where partial data were saved

    Returns:
        already aggregated responses
    """
    with path.open('rb') as file:
        partial_data = pickle.load(file)
    return partial_data


def _set_up_session(no_requests: int, path: Path = PARTIAL_PATH) -> Tuple[List, int, std.tqdm]:
    """
    Restores downloading session based on already saved data or sets up a new one
    Args:
        no_requests: total number of requests target
        path: path to partial data from previous session

    Returns:
        (tuple):
            data from previous session or initialized new ones
            starting iterator for request
            progress bar (new or from previous session)
    """
    if path.exists():
        logging.info('Restoring previous download session.')
        partial_data = _restore_partial_data()
        last_iteration = len(partial_data)
        progress_bar = tqdm(total=no_requests)
        progress_bar.update(last_iteration)
    else:
        logging.info('Initialising new download session.')
        partial_data, last_iteration, progress_bar = [], 0, tqdm(total=no_requests)
    return partial_data, last_iteration, progress_bar


def _get_resource_from_request(resource_request: request.Request) -> Dict:
    """
    Call for request to UMWaw API.
    Args:
        resource_request: formatted request

    Returns:
        validated response for resource_request
    """
    try:
        with request.urlopen(resource_request) as req:
            response = json.loads(req.read().decode())
            _validate_response(resource_request, response)
    except (error.URLError, error.HTTPError) as err:
        raise err

    return response


# pylint: disable=too-many-arguments
def _get_resource_over_time(resource_request: request.Request,
                            no_of_requests: int = 1,
                            interval_btwn_requests: int = 1,
                            attempts: int = 3,
                            keep_partial_if_fail: bool = True,
                            path: Path = PARTIAL_PATH) -> List:
    """
    Wrapper for _get_resource_from_request to iterate over time.
    Args:
        resource_request: formatted request
        no_of_requests: total number of requests target
        interval_btwn_requests: how many minutes to wait between requests
        attempts: how many times to attempt session restoration before failing
        keep_partial_if_fail: if partial data from failed attempt should be kept
        path: path to partial data storage

    Returns:
        list of aggregated validated responses for resource_request
    """
    if not (isinstance(no_of_requests, int)
            and isinstance(interval_btwn_requests, int)
            and isinstance(attempts, int)):
        raise TypeError('All numerical parameters must be positive integers.')
    if not (no_of_requests > 0 and interval_btwn_requests > 0 and attempts > 0):
        raise ValueError('All numerical parameters must be positive integers.')

    for attempt in range(attempts):
        logging.info('Attempt %s/%s.', attempt + 1, attempts)
        aggregated_results, i, pbar = _set_up_session(no_of_requests)

        while i < no_of_requests:
            try:
                if i != 0:
                    sleep(interval_btwn_requests * 60)
                response = _get_resource_from_request(resource_request)
                aggregated_results.append(response)
                pbar.update(1)
                i += 1
            except (error.HTTPError, error.URLError, KeyboardInterrupt):
                _store_partial_data(aggregated_results)
                logging.info('Attempt %s failed.', attempt + 1)
                break

        if len(aggregated_results) == no_of_requests:
            logging.info('Data collected in %s/%s attempts.', attempt + 1, attempts)
            path.unlink(missing_ok=True)
            return aggregated_results

    if not keep_partial_if_fail:
        path.unlink(missing_ok=True)
    raise RuntimeError(f'All attempts failed. Partial results stored in {path}')
# pylint: enable=too-many-arguments


def _validate_response(req: request.Request,
                       response: Dict) -> None:
    """
    Validate if response from UMWaw API is correct.
    Args:
        req: full request to UMWaw API
        response: obtained response for req
    """
    if 'result' not in response:
        raise error.HTTPError(url=req.full_url, code=204, fp=None, hdrs={}, msg='Empty data.')

    if 'error' in response or not isinstance(response['result'], list):
        msg = response['error'] if 'error' in response else response['result']
        raise error.HTTPError(url=req.full_url, code=400, fp=None, hdrs={}, msg=msg)
