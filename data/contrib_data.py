import logging

import requests

from community.git import get_org_name
from data.models import Contributor


def get_contrib_data():
    logger = logging.getLogger(__name__)
    IMPORT_URL = 'https://webservices.' + get_org_name() + '.io/contrib/'
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(
            url=IMPORT_URL,
            headers=headers,
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(e)
        return

    data = response.json()
    return data


def import_data(contributor):
    logger = logging.getLogger(__name__)
    login = contributor.get('login', None)
    try:
        contributor['issues_opened'] = contributor.pop('issues')
        contributor['num_commits'] = contributor.pop('contributions')
        c, create = Contributor.objects.get_or_create(
            **contributor
        )
        if create:
            c.save()
            logger.info('Contributor, %s has been saved.' % c)
    except Exception as ex:
        logger.error(
            'Something went wrong saving this contributor %s: %s'
            % (login, ex))
