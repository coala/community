import requests
import os

from .config import load_cache

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
        if task.__contains__('mentors'):
            del task['mentors']


def cleanse_tasks(tasks):
    tokens = {
        'GH_TOKEN': os.environ.get('GH_TOKEN'),
    }

    for task in tasks.values():
        if (task['max_instances'] == 1 and
                str(task['external_url']).__contains__('issues/')):
            task['state'] = get_task_state(task['external_url'], tokens)

    cleansed_tasks = published_tasks(tasks)

    strip_mentors(tasks)

    return cleansed_tasks


def get_task_state(task_url, tokens):
    if task_url.__contains__('github'):
        task_url = task_url.replace('github.com', 'api.github.com/repos')
        headers = {'Authorization': 'token {}'.format(tokens['GH_TOKEN'])}
    else:
        issue_id = task_url.split('issues/')[1]
        project_id = ((task_url.split('https://gitlab.com/')
                       [1]).split('/issues')[0]).replace('/', '%2F')
        task_url = 'https://gitlab.com/api/v4/projects/{}/issues/{}'.format(
            project_id, issue_id)
        headers = {}

    if tokens['GH_TOKEN']:
        task_data = requests.get(task_url, headers=headers).json()
    else:
        task_data = requests.get(task_url).json()

    if task_data['state'] == 'closed':
        task_state = 'COMPLETED'
    elif task_data['state'] == 'open' and len(task_data['assignees']) > 0:
        task_state = 'CLAIMED'
    else:
        task_state = 'AVAILABLE'

    return task_state
