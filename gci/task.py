from .config import load_cache

TASK_STATUS_DRAFT = 1
TASK_STATUS_PUBLISHED = 2

_tasks = None
_private_tasks = None
_tasks_by_url = None
_private_tasks_by_url = None


def get_tasks(private=False):
    global _tasks
    global _private_tasks

    if private:
        if _private_tasks is None:
            _private_tasks = load_cache('tasks.yaml', private=True)
            print(f'Loaded {len(_private_tasks)} private tasks')
        tasks = _private_tasks
    else:
        if _tasks is None:
            _tasks = load_cache('tasks.yaml')
            print(f'Loaded {len(_tasks)} tasks')
        tasks = _tasks

    return tasks


def index_tasks_by_url(private=False):
    global _tasks_by_url
    global _private_tasks_by_url

    if private:
        if _private_tasks_by_url is not None:
            return
        url_indexed_tasks = _private_tasks_by_url = {}

    else:
        if _tasks_by_url is not None:
            return
        url_indexed_tasks = _tasks_by_url = {}

    for task in get_tasks(private).values():
        if 'external_url' not in task:
            continue

        url = task['external_url']
        url_indexed_tasks[url] = task


def get_task(task_id, private=False):
    return get_tasks(private)[task_id]


def lookup_url(url, private=False):
    index_tasks_by_url(private)

    if private:
        index = _private_tasks_by_url
    else:
        index = _tasks_by_url

    return index.get(url)


def published_tasks(tasks):
    return dict(
        (task_id, task)
        for task_id, task
        in tasks.items()
        if task['status'] == TASK_STATUS_PUBLISHED
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
