import ruamel.yaml
import os
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'community.settings'

DATA_DIR = settings.STATIC_ROOT


def load_cache(filename):
    with open(os.path.join(DATA_DIR, filename), 'r') as f:
        return ruamel.yaml.load(f, Loader=ruamel.yaml.Loader)


def get_year():
    return 2018 - 1
