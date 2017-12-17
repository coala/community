import os
import os.path

from git.config import GitConfigParser
import giturlparse
import giturlparse.parser

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


def get_remote_url():
    """Obtain a parsed remote URL.

    Uses CI environment variables or git remotes.
    """
    # Netlify doesnt have any git remotes
    # It only sets the REPOSITORY_URL
    url = os.environ.get('REPOSITORY_URL')
    if not url:
        remote = get_config_remote()
        url = remote[0][1]

    try:
        url = giturlparse.parse(url)
    except giturlparse.parser.ParserError:
        url = giturlparse.parse(url + '.git')
    return url


def get_owner():
    """Obtain the owner of the repository.
    """
    url = get_remote_url()
    return url.owner
