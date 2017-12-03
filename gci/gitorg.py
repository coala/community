import re

from .config import get_api_key

from IGitt.GitHub.GitHub import GitHub, GitHubToken
from IGitt.GitLab.GitLab import GitLab, GitLabPrivateToken

_orgs = {}


class GitOrg():

    def __init__(self, name):
        self.name = name
        self.IGH = GitHub(GitHubToken(get_api_key('GH')))
        self.IGL = GitLab(GitLabPrivateToken(get_api_key('GL')))

        print('loading org %s' % name)
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
        print('loaded org %s' % name)

    def get_repo(self, repo_name):
        if repo_name not in self.REPOS:
            full_name = '%s/%s' % (self.name, repo_name)
            print('loading non-writable repo %s' % full_name)
            try:
                repo = self.IGH.get_repo(full_name)
                repo.identifier
                self.REPOS[repo_name] = repo
            except Exception:
                print('Unable to load GitHub repo %s' % full_name)
            try:
                repo = self.IGL.get_repo(full_name)
                repo.identifier
                self.REPOS[repo_name] = repo
            except Exception:
                print('Unable to load GitLab repo %s' % full_name)

        return self.REPOS[repo_name]


def get_org(name):
    if name not in _orgs:
        _orgs[name] = GitOrg(name)
    return _orgs[name]


def get_issue(url):
    match = re.match(r'https://(github|gitlab)\.com/'
                     r'([^/]+)/(.+)/issues/(\d+)',
                     url)
    if not match:
        print('not an issue %s' % url)
        return

    org_name = match.group(2)
    repo_name = match.group(3)
    issue_number = match.group(4)

    try:
        org = get_org(org_name)
    except Exception as e:
        print('Unable to load org %s: %s' % (org_name, e))
        return
    try:
        repo = org.get_repo(repo_name)
    except Exception as e:
        print('Unable to load %s repo %s: %s' % (org_name, repo_name, e))
        return
    try:
        issue = repo.get_issue(int(issue_number))
    except Exception as e:
        print('Unable to load issue %s' % url)
        return
    return issue
