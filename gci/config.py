import ruamel.yaml
import os
from community.settings import STATIC_ROOT
from community.config import get_api_key


__all__ = (
    'GCI_DATA_DIR',
    'get_api_key',
    'load_cache',
)

GCI_DATA_DIR = os.path.join(
    os.path.dirname(__file__), '..',
    STATIC_ROOT,
)


def load_cache(filename):
    with open(os.path.join(GCI_DATA_DIR, filename), 'r') as f:
        return ruamel.yaml.load(f, Loader=ruamel.yaml.Loader)
