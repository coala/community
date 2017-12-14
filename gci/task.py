from .config import load_cache

_tasks = {}


def get_tasks():
    global _tasks
    if not _tasks:
        _tasks = load_cache('tasks.yaml')

    return _tasks


def get_task(task_id):
    return get_tasks()[task_id]
