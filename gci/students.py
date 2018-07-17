import re
import logging

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
    logger = logging.getLogger(__name__ + '._get_tasks')
    client = get_client()
    page = 1

    while page > 0:
        try:
            tasks = client.ListTasks(page=page)
        except Exception as e:
            logger.error(e.response.content)
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
            student_data = {
                'id': student_id,
                'display_name': instance['student_display_name'],
                'organization_id': instance['organization_id'],
                'organization_name': instance['organization_name'],
                'program_year': instance['program_year'],
                'instances': [],
            }
            students[student_id] = student_data
            yield student_data
        else:
            student_data = students[student_id]

        student_data['instances'].append(instance)


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
    logger = logging.getLogger(__name__ + '.get_linked_students')
    for student in list(get_issue_related_students()):
        instances = student['instances']
        for instance in instances:
            task = get_task(instance['task_definition_id'])
            task_id = task['id']
            url = task['external_url']
            if not url:
                logger.info('task %d has no url' % task_id)
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
                    logger.info('task %d url not recognised: %s' %
                                (task_id, url))
                else:
                    if len(issue.assignees) == 0:
                        logger.info('task %d: No assignees for %s' %
                                    (task_id, url))
                    elif len(issue.assignees) > 1:
                        logger.info('task %d: Many assignees for %s: %s' %
                                    (task_id, url, ', '.join(issue.assignees)))
                    else:
                        student['username'] = list(issue.assignees)[0].username
                        print('student %s is %s because of %s' %
                              (student['id'], student['username'], url))
                        yield student
                        break

                    if len(issue.mrs_closed_by) == 0:
                        logger.info('task %d: No mrs closing %s' %
                                    (task_id, url))
                    elif len(issue.mrs_closed_by) == 0:
                        logger.info('task %d: Many mrs closing %s' %
                                    (task_id, url))
                    else:
                        mr = list(issue.mrs_closed_by)[0]
                        user = mr.author

                        student['username'] = user.username
                        print('student %s is %s because of %s (from PR)' %
                              (student['id'], student['username'], url))
                        yield student
                        break
