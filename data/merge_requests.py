import logging
from dateutil.parser import parse
import pytz

import requests

from data.models import (
    MergeRequest,
    Label,
    IssueNumber,
    Contributor,
    )
from data.newcomers import active_newcomers
from data.webservices import webservices_url


def fetch_mrs(hoster):
    """
    Get mrs opened by newcomers.

    :param hoster: a string representing hoster, e.g. 'GitHub'
    :return: a json of mrs data
    """
    logger = logging.getLogger(__name__)
    hoster = hoster.lower()
    import_url = webservices_url('mrs/%s/all' % hoster)

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
    mrs = response.json()

    # Removing mrs which are not opened by newcomers
    mrs_list = []
    for mr in mrs:
        if mr['author'] in active_newcomers():
            mrs_list.append(mr)
    return mrs_list


def import_mr(hoster, mr):
    """
    Import mr data to database.

    :param hoster: a string representing hoster
    :param mr: a dict containing mr's data
    """
    logger = logging.getLogger(__name__)
    number = mr.get('number')
    assignees = mr.pop('assignees')
    labels = mr.pop('labels')
    author = mr.pop('author')
    repo_id = mr['repo_id']
    closes_issues = mr.pop('closes_issues')

    # Parse string datetime to datetime object and add timezone support
    mr['created_at'] = pytz.utc.localize(parse(mr['created_at']))
    mr['updated_at'] = pytz.utc.localize(parse(mr['updated_at']))

    try:
        author, created = Contributor.objects.get_or_create(login=author)
        mr['author'] = author
        mr['hoster'] = hoster
        mr_object, created = MergeRequest.objects.get_or_create(**mr)

        # Saving assignees
        assignee_objects_list = []
        for assignee in assignees:
            assignee_object, created = Contributor.objects.get_or_create(
                login=assignee)
            assignee_objects_list.append(assignee_object)
        mr_object.assignees.add(*assignee_objects_list)

        # Saving issues closes by this mr
        closes_issues_list = []
        for i_number in closes_issues:
            issue_number_object, created = (
                IssueNumber.objects.get_or_create(
                    number=i_number,
                    repo_id=repo_id))
            closes_issues_list.append(issue_number_object)
        mr_object.closes_issues.add(*closes_issues_list)

        # Saving labels on the mr
        label_objects_list = []
        for label in labels:
            label_object, created = Label.objects.get_or_create(name=label)
            label_objects_list.append(label_object)
        mr_object.labels.add(*label_objects_list)
        logger.info('MR: %s has been saved.' % mr_object)
    except Exception as ex:
        logger.error(
            'Something went wrong saving this mr %s: %s'
            % (number, ex))
