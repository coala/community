import os

API_KEY_FILE = '.%s_API_KEY'


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
        print('Please put your %s API key at %s.' % (name, filename))
        exit(1)
