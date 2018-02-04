from .config import load_cache


_org = {}
_projects = {}


def get_org_data():
    global _org
    if not _org:
        _org = load_cache('gsoc_org_info.yaml')

    return _org


def get_projects_data():
    global _projects
    if not _projects:
        _projects = load_cache('gsoc_project_info.yaml')

    return _projects
