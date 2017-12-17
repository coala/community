import ruamel.yaml
import os

API_KEY_FILE = '.%s_API_KEY'

GCI_DATA_DIR = os.path.join(
    os.path.dirname(__file__), '..',
    '_site',
)


class TokenMissing(KeyError):
    """The requested token is not available.
    """


def get_api_key(name):
    env_val = os.environ.get('%s_TOKEN' % name)
    if env_val:
        return env_val

    homedir = os.path.expanduser('~')
    filename = API_KEY_FILE % name

    try:
        with open(os.path.join(homedir, filename)) as api_key_file:
            api_key = api_key_file.readline().strip()
            return api_key
    except IOError:
        raise TokenMissing('Please put your %s API key at %s.' %
                           (name, filename))


def load_cache(filename):
    with open(os.path.join(GCI_DATA_DIR, filename), 'r') as f:
        return ruamel.yaml.load(f, Loader=ruamel.yaml.Loader)
