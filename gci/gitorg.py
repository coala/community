import collections
import re
import logging

import requests

from community.git import get_irepo


# Matches structure of git-url-parse
IssueRepoUrl = collections.namedtuple('Parsed', [
    'resource',
    'user',
    'owner',
    'name',
])

_repos = {}


def get_repo(url):
    if url not in _repos:
        _repos[url] = get_irepo(url)
    return _repos[url]


def get_issue(url):
    logger = logging.getLogger(__name__ + '.get_issue')
    match = re.match(r'https://(github|gitlab)\.com/'
                     r'([^/]+)/(.+)/issues/(\d+)',
                     url)
    if not match:
        logger.info('not an issue %s' % url)
        return

    resource = match.group(1) + '.com'
    org_name = match.group(2)
    repo_name = match.group(3)
    issue_number = match.group(4)

    issue_url = IssueRepoUrl(
        resource,
        org_name,
        org_name,
        repo_name,
    )

    try:
        repo = get_repo(issue_url)
    except Exception as e:
        logger.error('Unable to load %s repo %s: %s' % (org_name, repo_name, e))
        return
    try:
        issue = repo.get_issue(int(issue_number))
    except Exception as e:
        logger.error('Unable to load issue %s: %s' % (url, e))
        return
    return issue


def get_logo(org_name, size=0):
    if size != 0:
        image_url = 'http://github.com/%s.png?size=%s' % (org_name, size)
    else:
        image_url = 'http://github.com/%s.png' % (org_name)

    return requests.get(image_url).content
