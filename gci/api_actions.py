import logging
import pprint

# Start ignoring KeywordBear
from coala_utils.Question import ask_yes_no
# Stop ignoring

from gci.client import GCIAPIClient
from gci.config import get_api_key
from gci.config import load_yaml
from gci.gitorg import get_issue
from gci.issues import check_task
from gci.issues import get_projects
from gci.issues import lookup_url

_mentor_config = None


def get_mentor_config(filename):
    global _mentor_config

    if not _mentor_config:
        _mentor_config = load_yaml(filename)

    return _mentor_config


def allocate_mentors(task, mentor_config_filename):
    mentor_config = get_mentor_config(mentor_config_filename)
    for tag in task['tags']:
        mentors = mentor_config.get(tag)
        if mentors:
            task['mentors'].extend(mentors)

    url = task['external_url']
    for key, mentors in mentor_config.items():
        if key in url.lower():
            task['mentors'].extend(mentors)


def upload_tasks(tasks, mentor_config_filename):
    logger = logging.getLogger(__name__ + '.upload_tasks')
    client = GCIAPIClient(get_api_key('GCI'))

    for task in tasks:
        url = task['external_url']

        if not check_task(task):
            logger.warning(f'task check failed: {url}')
            continue

        existing_task = lookup_url(url, private=True)
        if existing_task:
            task_id = existing_task['id']
            logger.warning(f'{url} is task {task_id}')
            continue

        if not task['mentors'] and mentor_config_filename:
            allocate_mentors(task, mentor_config_filename)

        if task['status'] == 2 and not task['mentors']:
            logger.warning(f'{url}: Can not publish without mentors')
            continue

        pprint.pprint(task)
        if task['mentors']:
            if ask_yes_no(f'Publish task', 'no'):
                task['status'] = 2

        if task['status'] != 2:
            if not ask_yes_no(f'Create task', 'no'):
                continue

        client.NewTask(task)

        if task['status'] == 2:
            print('Task published.')
        else:
            print('Task created.')


def publish_tasks(tasks, issue_config, mentor_config_filename):
    client = GCIAPIClient(get_api_key('GCI'))
    projects = dict(get_projects(issue_config, yield_levels=False))

    for task_id, task in tasks.items():
        name = task['name']

        if 'status' in task:
            publish_flag = task['status']
            if publish_flag == 2:
                # TODO: unpublishing tasks if project disabled/blocked
                continue
            assert publish_flag == 1

        if not task['tags']:
            continue

        url = task['external_url']
        if not url:
            print(f'{task_id} {name} has no url')
            continue
        issue = get_issue(url)
        if not issue:
            print(f'{task_id} {name} {url} not recognised')
            continue

        project = projects.get(issue.repository.full_name.lower())

        if not project:
            print(f'{task_id} {url} project not recognised')
            continue

        disabled = project.get('disabled')
        if disabled:
            print(f'{task_id} {url} project disabled')
            continue

        repo_block = project.get('blocked')
        if repo_block and issue.number != repo_block:
            print(f'{task_id} {url} project blocked by {repo_block}')
            continue

        if not task['mentors'] and mentor_config_filename:
            allocate_mentors(task, mentor_config_filename)

            if not task['mentors']:
                print(f'{task_id} {url} no mentors available')
                continue

        task['status'] = 2

        pprint.pprint(task)
        if not ask_yes_no(f'Publish task {task_id}', 'no'):
            continue

        print(f'Publishing {task_id} {name} ..')
        client.UpdateTask(task_id, task)
