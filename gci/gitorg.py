import re
import logging

from .config import get_api_key

from IGitt.GitHub.GitHub import GitHub, GitHubToken
from IGitt.GitLab.GitLab import GitLab, GitLabPrivateToken

import requests

_orgs = {}


class GitOrg():

    def __init__(self, name):
        logger = logging.getLogger(__name__ + '.__init__')
        self.name = name
        self.IGH = GitHub(GitHubToken(get_api_key('GH')))
        self.IGL = GitLab(GitLabPrivateToken(get_api_key('GL')))

        logger.info('loading org %s' % name)
        self.REPOS = dict()

        self.gh_repos = {repo.full_name.split('/')[-1]: repo for repo in
                         filter(lambda x: (x.full_name.split('/')[0] ==
                                           self.name),
                                self.IGH.write_repositories)}
        self.REPOS.update(self.gh_repos)

        self.gl_repos = {repo.full_name.split('/')[-1]: repo for repo in
                         filter(lambda x: (x.full_name.split('/')[0] ==
                                           self.name),
                                self.IGL.write_repositories)}
        self.REPOS.update(self.gl_repos)
        logger.info('loaded org %s with %d repositories' %
                    (name, len(self.REPOS)))

    def get_repo(self, repo_name):
        logger = logging.getLogger(__name__ + '.get_repo')
        if repo_name not in self.REPOS:
            full_name = '%s/%s' % (self.name, repo_name)
            logger.info('loading non-writable repo %s' % full_name)
            try:
                repo = self.IGH.get_repo(full_name)
                # Use `clone_url` to ensure the repository is usable
                repo.clone_url
                self.REPOS[repo_name] = repo
                logger.info('loaded non-writable GitHub repo %s' % full_name)

                return repo
            except Exception as e:
                logger.error('Unable to load GitHub repo %s: %s' %
                             (full_name, e))
            try:
                repo = self.IGL.get_repo(full_name)
                # Use `clone_url` to ensure the repository is usable
                repo.clone_url
                logger.info('loaded non-writable GitLab repo %s' % full_name)
                self.REPOS[repo_name] = repo
            except Exception as e:
                logger.error('Unable to load GitLab repo %s: %s' %
                             (full_name, e))

        return self.REPOS[repo_name]


def get_org(name):
    if name not in _orgs:
        _orgs[name] = GitOrg(name)
    return _orgs[name]


def get_issue(url):
    logger = logging.getLogger(__name__ + '.get_issue')
    match = re.match(r'https://(github|gitlab)\.com/'
                     r'([^/]+)/(.+)/issues/(\d+)',
                     url)
    if not match:
        logger.info('not an issue %s' % url)
        return

    org_name = match.group(2)
    repo_name = match.group(3)
    issue_number = match.group(4)

    try:
        org = get_org(org_name)
    except Exception as e:
        logger.error('Unable to load org %s: %s' % (org_name, e))
        return
    try:
        repo = org.get_repo(repo_name)
    except Exception as e:
        logger.error('Unable to load %s repo %s: %s' % (org_name, repo_name, e))
        return
    try:
        issue = repo.get_issue(int(issue_number))
    except Exception as e:
        logger.error('Unable to load issue %s' % url)
        return
    return issue


def get_logo(org_name, size=0):
    if size != 0:
        image_url = 'http://github.com/%s.png?size=%s' % (org_name, size)
    else:
        image_url = 'http://github.com/%s.png' % (org_name)

    return requests.get(image_url).content
