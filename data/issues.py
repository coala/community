import logging
from dateutil.parser import parse
import pytz

import requests

from data.models import (
    Issue,
    Label,
    Contributor,
    )
from data.newcomers import active_newcomers
from data.webservices import webservices_url


def fetch_issues(hoster):
    """
    Get issues opened by newcomers.

    :param hoster: a string representing hoster, e.g. 'GitHub'
    :return: a json of issues data
    """
    logger = logging.getLogger(__name__)
    hoster = hoster.lower()
    import_url = webservices_url('issues/%s/all' % hoster)

    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(
            url=import_url,
            headers=headers,
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(e)
        return
    issues = response.json()

    # Removing issues which are not opened by newcomers
    issues_list = []
    for issue in issues:
        if issue['author'] in active_newcomers():
            issues_list.append(issue)
    return issues_list


def import_issue(hoster, issue):
    """
    Import issue data to database.

    :param hoster: a string representing hoster
    :param issue: a dict containing issue's data
    """
    logger = logging.getLogger(__name__)
    number = issue.get('number')
    assignees = issue.pop('assignees')
    labels = issue.pop('labels')
    author = issue.pop('author')

    # Parse string datetime to datetime object and add timezone support
    issue['created_at'] = pytz.utc.localize(parse(issue['created_at']))
    issue['updated_at'] = pytz.utc.localize(parse(issue['updated_at']))

    try:
        author, created = Contributor.objects.get_or_create(login=author)
        issue['author'] = author
        issue['hoster'] = hoster
        issue_object, created = Issue.objects.get_or_create(**issue)

        # Saving assignees
        assignee_objects_list = []
        for assignee in assignees:
            assignee_object, created = Contributor.objects.get_or_create(
                login=assignee)
            assignee_objects_list.append(assignee_object)
        issue_object.assignees.add(*assignee_objects_list)

        # Saving labels
        label_objects_list = []
        for label in labels:
            label_object, created = Label.objects.get_or_create(name=label)
            label_objects_list.append(label_object)
        issue_object.labels.add(*label_objects_list)
        logger.info('Issue: %s has been saved.' % issue_object)
    except Exception as ex:
        logger.error(
            'Something went wrong saving this issue %s: %s'
            % (number, ex))
