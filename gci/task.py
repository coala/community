from .config import load_cache

_tasks = {}


def get_tasks():
    global _tasks
    if not _tasks:
        _tasks = load_cache('tasks.yaml')

    return _tasks


def get_task(task_id):
    return get_tasks()[task_id]


def published_tasks(tasks):
    return dict(
        (task_id, task)
        for task_id, task
        in tasks.items()
        if task['status'] == 2
    )


def beginner_tasks(tasks):
    return dict(
        (task_id, task)
        for task_id, task
        in tasks.items()
        if task['is_beginner']
    )


def strip_mentors(tasks):
    for task in tasks.values():
        del task['mentors']


def cleanse_tasks(tasks):
    cleansed_tasks = published_tasks(tasks)

    strip_mentors(tasks)

    return cleansed_tasks
