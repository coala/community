import os
import re

from .client import GCIAPIClient

from .config import get_api_key, load_cache
from .gitorg import get_issue
from .task import get_task

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


def get_effective_students(students):
    for student in list(students):
        instances = student['instances']
        instances = [instance for instance in instances
                     if instance['status'] != 'ABANDONED']
        if instances:
            yield student


def get_issue_related_students(students):
    for student in list(get_effective_students(students)):
        instances = student['instances']
        for instance in instances:
            task = get_task(instance['task_definition_id'])
            if task['external_url']:
                if 'issues' in task['external_url']:
                    yield student
                    break


def get_linked_students(students):
    for student in list(get_issue_related_students(students)):
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
                issue = get_issue(url)
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
                        yield student
                        break
