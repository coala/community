import os
import os.path

from git.config import GitConfigParser
import giturlparse
import giturlparse.parser
from IGitt.GitHub.GitHub import GitHub, GitHubToken
from IGitt.GitLab.GitLab import GitLab, GitLabPrivateToken

from .config import get_api_key

REPO_DIR = os.path.join(
    os.path.dirname(__file__),
    '..',
)
GIT_CONFIG = os.path.join(
    REPO_DIR,
    '.git',
    'config',
)

_config = None
_org_name = None
_IGH = None
_IGL = None


def get_config():
    global _config
    if not _config:
        _config = GitConfigParser(GIT_CONFIG)
    return _config


def get_config_remote(name='origin'):
    config = get_config()

    has_remote = False

    for key in config.sections():
        if key == 'remote "%s"' % name:
            return config.items(key)
        elif key.startswith('remote'):
            has_remote = True

    if has_remote:
        raise KeyError('No git remote called "%s"' % name)

    raise KeyError('No git remotes found')


def get_remote_url(name='origin'):
    """Obtain a parsed remote URL.

    Uses CI environment variables or git remotes.
    """
    # Netlify doesnt have any git remotes
    # It only sets the REPOSITORY_URL
    url = os.environ.get('REPOSITORY_URL')
    if not url:
        remote = get_config_remote(name)
        assert remote[0][0] == 'url'
        url = remote[0][1]

    try:
        url = giturlparse.parse(url)
    except giturlparse.parser.ParserError:
        url = giturlparse.parse(url + '.git')
    return url


def get_repo_slug(url):
    """Obtain the slug of the repository URL.
    """
    return url.owner + '/' + url.name


def get_owner():
    """Obtain the owner of the repository.
    """
    url = get_remote_url()
    return url.owner


def get_ihoster(url):
    global _IGH, _IGL
    if url.resource == 'github.com':
        if not _IGH:
            # Allow unauthenticated requests
            try:
                token = get_api_key('GH')
            except Exception:
                token = None
            _IGH = GitHub(GitHubToken(token))
        return _IGH
    elif url.resource == 'gitlab.com':
        if not _IGL:
            # https://gitlab.com/gitmate/open-source/IGitt/issues/114
            _IGL = GitLab(GitLabPrivateToken(get_api_key('GL')))

        return _IGL


def get_irepo(url=None):
    if not url:
        url = get_remote_url()

    hoster = get_ihoster(url)
    slug = get_repo_slug(url)
    repo = hoster.get_repo(slug)
    return repo


def get_parent_repo(url=None):
    """Obtain the parent repository of the current repository.

    Return: None if it has no parent
    """
    repo = get_irepo(url)
    return repo.parent


def get_parent_slug(url=None):
    parent = get_parent_repo(url)
    if parent:
        return parent.full_name


def get_org_name():
    global _org_name
    if _org_name:
        return _org_name

    repo = get_irepo()
    # Travis Pull Requests do not have tokens, and unauthenticated use
    # of GitHub API will result in API rate limit errors
    if os.environ.get('TRAVIS_PULL_REQUEST', 'false') == 'false':
        if repo.parent:
            repo = repo.parent

    _org_name = repo.full_name.split('/', 1)[0]
    return _org_name


def get_upstream_repo():
    """Obtain the parent slug of the repository.
    """
    try:
        remote = get_remote_url(name='origin')
    except KeyError:
        remote = None

    parent = get_parent_repo(remote)
    if not parent:
        raise RuntimeError('Parent repo not found')
    return parent


def get_deploy_url(name=None, hoster=None):
    """
    Obtain the http where deploys appear.
    When `name` is None, fetch current repo of current org,
    otherwise, fetch a specified repo of current org.
    """
    # Use environment variable URL when Netlify detected
    if not name and os.environ.get('REPOSITORY_URL'):
        return os.environ.get('URL')

    url = get_remote_url()

    owner = url.owner
    path = name if name else url.name
    if hoster is not None:
        deploy_url = 'https://%s.%s.io/%s' % (owner, hoster, path)
    elif url.resource == 'github.com':
        deploy_url = 'https://%s.github.io/%s' % (owner, path)
    elif url.resource == 'gitlab.com':
        deploy_url = 'https://%s.gitlab.io/%s' % (owner, path)
    else:
        raise Exception('remote %s is not supported' % url)

    return deploy_url


def get_upstream_deploy_url(name=None, hoster='github'):
    """
    Obtain the http where the upstream deploys appear.
    When `name` is None, fetch current repo of current org,
    otherwise, fetch a specified repo of current org.
    """
    repo = get_upstream_repo()
    owner, _, repo_name = repo.full_name.partition('/')
    path = name if name else repo_name
    deploy_url = 'https://%s.%s.io/%s' % (owner, hoster, path)

    return deploy_url
