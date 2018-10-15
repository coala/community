import ruamel.yaml
import os
from community.settings import STATIC_ROOT
from community.config import get_api_key

__all__ = (
    'GCI_DATA_DIR',
    'GCI_PRIVATE_DATA_DIR',
    'GCI_PRIVATE_DATA_ROOT',
    'get_api_key',
    'load_cache',
)

GCI_PRIVATE_DATA_ROOT = 'private'

GCI_DATA_DIR = os.path.join(
    os.path.dirname(__file__), '..',
    STATIC_ROOT,
)

GCI_PRIVATE_DATA_DIR = os.path.join(
    os.path.dirname(__file__), '..',
    GCI_PRIVATE_DATA_ROOT,
)


def load_cache(filename, private=False):
    if private:
        data_dir = GCI_PRIVATE_DATA_ROOT
    else:
        data_dir = GCI_DATA_DIR

    path = os.path.join(data_dir, filename)
    with open(path, 'r') as f:
        return ruamel.yaml.load(f, Loader=ruamel.yaml.Loader)
