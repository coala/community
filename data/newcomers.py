from functools import lru_cache

import requests

from data.webservices import webservices_url


@lru_cache(maxsize=32)
def active_newcomers():
    """
    Get the list of newcomers active in the last three months.

    :return: the list of newcomer usernames
    """
    NEWCOMERS_URL = webservices_url('newcomers/active')
    response = requests.get(NEWCOMERS_URL)
    response.raise_for_status()
    newcomers = response.json()
    active_newcomers_list = []
    for newcomer in newcomers:
        active_newcomers_list.append(newcomer['username'])
    return active_newcomers_list
