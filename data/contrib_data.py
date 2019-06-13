import logging

import requests

from data.models import Contributor, Team
from data.webservices import webservices_url


def get_contrib_data():
    logger = logging.getLogger(__name__)
    IMPORT_URL = webservices_url('contrib')

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
    teams = contributor.get('teams')
    try:
        contributor['issues_opened'] = contributor.pop('issues')
        contributor['num_commits'] = contributor.pop('contributions')
        contributor['image_url'] = get_image_url(login)
        contributor.pop('teams')
        c, create = Contributor.objects.get_or_create(
            **contributor
        )
        if create:
            for team in teams:
                t, created = Team.objects.get_or_create(name=team)
                c.teams.add(t)
            logger.info('Contributor, %s has been saved.' % c)
    except Exception as ex:
        logger.error(
            'Something went wrong saving this contributor %s: %s'
            % (login, ex))


def get_image_url(username):
    return 'https://avatars1.githubusercontent.com/{}'.format(username)
