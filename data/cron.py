import json
from collections import defaultdict
from time import sleep

import requests
from IGitt.GitHub import GitHub

from coala_web.settings import GITHUB_API_KEY
from org.models import Contributor

request_headers = {'Authorization': 'token %s' % GITHUB_API_KEY}


def fetch_org():
    data = defaultdict(lambda: defaultdict(int, {'name': '', 'bio': ''}))
    repo_url = '/orgs/coala/repos'
    response_repo = GitHub.get(GITHUB_API_KEY, repo_url)
    for repo in response_repo:
        commit_data = get_commits(repo, data)
        data = get_issues(repo, commit_data)

    for contributor in data:
        response = \
            requests.get('https://api.github.com/search/issues?q=commenter:' +
                         contributor + '%20is:pr%20user:coala',
                         headers=request_headers, timeout=3000)
        r_json = json.loads(response.text)
        data[contributor]['reviews'] = r_json['total_count']
        if int(response.headers['X-RateLimit-Remaining']) == 1:
            sleep(60)

    for contributor in data:
        user = GitHub.get(GITHUB_API_KEY, '/users/' + contributor)
        if user['bio']:
            data[contributor]['bio'] = user['bio']
        if user['name']:
            data[contributor]['name'] = user['name']

    # Saving dict in database
    for contributor in data:
        if Contributor.objects.filter(login=contributor).exists():
            c = Contributor.objects.get(login=contributor)
        else:
            c = Contributor()
            c.login = contributor
        c.name = data[contributor]['name']
        c.bio = data[contributor]['bio']
        c.num_commits = data[contributor]['contributions']
        c.issues_opened = data[contributor]['issues']
        c.reviews = data[contributor]['reviews']
        c.save()


def get_commits(repo, data):
    url = '/repos/coala/' + repo['name'] + '/contributors'
    response = GitHub.get(GITHUB_API_KEY, url)
    for contributor in response:
        data[contributor['login']]['contributions'] +=\
            contributor['contributions']
    return data


def get_issues(repo, data):
    url = '/repos/coala/' + repo['name'] + '/issues'
    response = GitHub.get(GITHUB_API_KEY, url)
    for issue_author in response:
        data[issue_author['user']['login']]['issues'] += 1
    return data
