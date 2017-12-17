import os
import re

from .client import GCIAPIClient

from .config import get_api_key, load_cache
from .gitorg import get_issue
from .task import beginner_tasks, get_task

PRIVATE_INSTANCE_STATUSES = (
    'ABANDONED',
    'OUT_OF_TIME',
    'PENDING_PARENTAL_CONSENT',
    'UNASSIGNED_BY_MENTOR',
)

PRIVATE_INSTANCE_ATTRIBUTES = (
    'modified',
    'deadline',
)

_client = None
_instances = {}


def get_client():
    global _client
    if _client:
        return _client
    _client = GCIAPIClient(get_api_key('GCI'))
    return _client


def _get_tasks():
    client = get_client()
    page = 1

    while page > 0:
        try:
            tasks = client.ListTasks(page=page)
        except Exception as e:
            print(e.response.content)
            raise

        for t in tasks['results']:
            yield t

        page = 0
        if tasks['next']:
            result = re.search(r'page=(\d+)', tasks['next'])
            if result:
                page = int(result.group(1))


def _get_instances():
    client = get_client()
    page = 1

    while page > 0:
        instances = client.ListTaskInstances(page=page)
        for instance in instances['results']:
            yield instance

        page = 0
        if instances['next']:
            result = re.search(r'page=(\d+)', instances['next'])
            if result:
                page = int(result.group(1))


def get_instances():
    global _instances
    if not _instances:
        _instances = load_cache('instances.yaml')

    return _instances


def cleanse_instances(instances, tasks):
    cleansed_instances = dict(
        (instance_id, instance)
        for instance_id, instance
        in instances.items()
        if instance['status'] not in PRIVATE_INSTANCE_STATUSES
        and instance['task_definition_id'] in tasks
        and instance['task_definition_id'] not in beginner_tasks(tasks)
    )

    for instance in cleansed_instances.values():
        if instance['status'] != 'COMPLETED':
            instance['status'] = 'CLAIMED'
            for key in PRIVATE_INSTANCE_ATTRIBUTES:
                del instance[key]

    return cleansed_instances


def get_students():
    students = {}
    for _, instance in get_instances().items():
        student_id = instance['student_id']
        if student_id not in students:
            student = {
                'id': student_id,
                'display_name': instance['student_display_name'],
                'organization_id': instance['organization_id'],
                'organization_name': instance['organization_name'],
                'program_year': instance['program_year'],
                'instances': [],
            }
            students[student_id] = student
            yield student
        else:
            student = students[student_id]

        student['instances'].append(instance)


def get_issue_related_students():
    for student in list(get_students()):
        instances = student['instances']
        for instance in instances:
            task = get_task(instance['task_definition_id'])
            if task['external_url']:
                if 'issues' in task['external_url']:
                    yield student
                    break


def get_linked_students():
    for student in list(get_issue_related_students()):
        instances = student['instances']
        for instance in instances:
            task = get_task(instance['task_definition_id'])
            task_id = task['id']
            url = task['external_url']
            if not url:
                print('task %d has no url' % task_id)
            elif '/wiki/' in url:
                pass
            else:
                try:
                    issue = get_issue(url)
                    # Ensure assignees works before continuing
                    issue.assignees
                except Exception as e:
                    print('Failed to load task %d url %s: %s' %
                          (task_id, url, e))
                    continue
                if not issue:
                    print('task %d url not recognised: %s' % (task_id, url))
                else:
                    if len(issue.assignees) == 0:
                        print('task %d: No assignees for %s' % (task_id, url))
                    elif len(issue.assignees) > 1:
                        print('task %d: Many assignees for %s: %s' %
                              (task_id, url, ', '.join(issue.assignees)))
                    else:
                        student['username'] = issue.assignees[0]
                        print('student %s is %s because of %s' %
                              (student['id'], issue.assignees[0], url))
                        yield student
                        break
