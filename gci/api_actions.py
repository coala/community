import logging
import pprint

# Start ignoring KeywordBear
from coala_utils.Question import ask_yes_no
# Stop ignoring

from community.diff import print_differences

from gci.client import GCIAPIClient
from gci.config import get_api_key
from gci.config import load_yaml
from gci.gitorg import get_issue
from gci.issues import check_task
from gci.issues import generate_task
from gci.issues import get_issue_metadata
from gci.issues import issue_is_available
from gci.issues import issue_is_blocked
from gci.issues import lookup_url
from gci.task import TASK_STATUS_DRAFT, TASK_STATUS_PUBLISHED

_mentor_config = None


def get_mentor_config(filename):
    global _mentor_config

    if not _mentor_config:
        _mentor_config = load_yaml(filename)

    return _mentor_config


def allocate_mentors(task, mentor_config_filename):
    mentor_config = get_mentor_config(mentor_config_filename)
    # Start ignoring PyPluralNamingBear
    if 'mentors' not in task:
        task['mentors'] = []

    for tag in task.get('tags'):
        mentors = mentor_config.get(tag)
        if mentors:
            task['mentors'].extend(mentors)

    url = task['external_url']
    for key, mentors in mentor_config.items():
        if key in url.lower():
            task['mentors'].extend(mentors)
    # Stop ignoring


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

        if task['status'] == TASK_STATUS_PUBLISHED and not task['mentors']:
            logger.warning(f'{url}: Can not publish without mentors')
            continue

        pprint.pprint(task)
        if task['mentors']:
            if ask_yes_no(f'Publish task', 'no'):
                task['status'] = TASK_STATUS_PUBLISHED

        if task['status'] != TASK_STATUS_PUBLISHED:
            if not ask_yes_no(f'Create task', 'no'):
                continue
            task['status'] = TASK_STATUS_DRAFT

        client.NewTask(task)

        if task['status'] == TASK_STATUS_PUBLISHED:
            print('Task published.')
        else:
            print('Task created.')


def update_issue_tasks(tasks, issue_config, mentor_config_filename, all_tasks):
    logger = logging.getLogger(__name__ + '.update_issue_tasks')
    client = GCIAPIClient(get_api_key('GCI'))

    # These are ordered to show highest 'impact' changes first, so these
    # do not need to be repeated in order to explain lower impact changes.
    manual_ordered_keys = ['tags', 'categories', 'mentors']

    for task_id, task in tasks.items():
        name = task['name']

        print(f'Checking {task_id} {name}')

        status = task['status']
        assert status in (TASK_STATUS_DRAFT, TASK_STATUS_PUBLISHED)

        if not check_task(task):
            logger.warning(f'existing task check failed: {task_id}')
            continue

        url = task['external_url']
        if not url:
            print(f'{task_id} {name} has no url')
            continue
        issue = get_issue(url)
        if not issue:
            print(f'{task_id} {name} {url} not recognised')
            continue

        try:
            issue_metadata = get_issue_metadata(issue_config, issue)
        except (RuntimeError, IndexError, ValueError) as e:
            print(f'{task_id} {name} {url}: {e}')
            continue

        updated_task = generate_task(issue, issue_metadata)

        if not updated_task:
            updated_task = task.copy()
            if task['status'] != TASK_STATUS_PUBLISHED:
                if not all_tasks:
                    continue

            updated_task['status'] = TASK_STATUS_DRAFT

        if not check_task(updated_task):
            logger.warning(f'task check failed: {task_id}')
            if task['status'] != TASK_STATUS_PUBLISHED:
                if not all_tasks:
                    continue

            updated_task['status'] = TASK_STATUS_DRAFT

            new_tags = updated_task['tags']
            if len(new_tags) > 5:
                print(f'Ignoring {task_id} {len(new_tags)} tags; using old')
                updated_task['tags'] = task['tags']

        if mentor_config_filename:
            allocate_mentors(updated_task, mentor_config_filename)
            # Allow self-assignment in GCI system
            old_mentors = set(task['mentors'])
            new_mentors = set(updated_task['mentors'])
            if old_mentors > new_mentors:
                updated_task['mentors'] = old_mentors

        if issue_is_blocked(issue, issue_metadata):
            # Dont consider updating blocked issues
            if task['status'] == TASK_STATUS_DRAFT:
                if not all_tasks:
                    continue

            updated_task['status'] = TASK_STATUS_DRAFT
        else:
            if not issue_is_available(issue, issue_metadata):
                # TODO: more carefully checking of task status,
                # after community issue #66
                if not all_tasks:
                    continue

                updated_task['status'] = TASK_STATUS_DRAFT

            if not updated_task.get('status'):
                if updated_task['mentors'] and updated_task['tags']:
                    updated_task['status'] = TASK_STATUS_PUBLISHED

        print(f'Comparing {task_id} {url} {name}')

        if type(task.get('mentors')) is list:
            task['mentors'] = set(task['mentors'])
        if type(updated_task.get('mentors')) is list:
            updated_task['mentors'] = set(updated_task['mentors'])
        changed = print_differences(task, updated_task,
                                    manual_ordered_keys)

        if not changed:
            continue

        if status == updated_task['status']:
            if status == TASK_STATUS_PUBLISHED:
                action = 'Update published'
            else:
                action = 'Update draft'
        elif updated_task['status'] == TASK_STATUS_DRAFT:
            action = 'Un-publish'
        else:
            action = 'Publish'

        if not ask_yes_no(f'{action} task {task_id}', 'no'):
            if action in ('Publish', 'Un-publish') and all_tasks:
                if not ask_yes_no(f'Edit task {task_id}', 'no'):
                    continue
                updated_task['status'] = status
            else:
                continue

        if action.startswith('Update '):
            actioning = action.replace('Update', 'Updating')
        else:
            actioning = action.replace('ublish', 'ublishing')

        print(f'{actioning} {task_id} {name} ..')
        try:
            for key in ['mentors', 'tags', 'categories']:
                updated_task[key] = list(updated_task[key])
            client.UpdateTask(task_id, updated_task)
            actioned = actioning.replace('ing ', 'ed ')
            print(f'{actioned} {task_id} {name}')
        except Exception as e:
            logger.warning(f'Failed to update: {e}')
            pass
