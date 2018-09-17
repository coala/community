import logging
import pprint

from .client import GCIAPIClient
from .config import get_api_key
from .gitorg import get_issue

from .task import lookup_url

from community.git import get_org_name

org_name = get_org_name()

unsuitable_labels = {
    'status/blocked',
    'status/invalid',
    'status/needs info',
    'status/needs design',
}

gci_labels = {
    'initiatives/gci',
    'initiative/gci',
    'googlecodein',
}

difficulty_level_names = ['newcomer', 'low', 'medium', 'high', 'extreme']

MAX_TAGS = 5


def issue_is_available(issue):
    logger = logging.getLogger(__name__ + '.issue_is_available')

    issue_id = issue.number
    url = issue.web_url

    if str(issue.state) in ('closed', ):
        logger.info(f'{issue_id}: {issue.state}')
        return False

    if str(issue.state) not in ('open', ):
        logger.warning(f'{url}: Unexpected state {issue.state}')
        return False

    if issue.assignees:
        logger.warning(f'Skipping {url} assigned to {issue.assignees}')
        return False

    logger.debug(pprint.pprint(issue))

    assert issue.title

    label_names = issue.labels

    wrong_labels = set(label_names).intersection(unsuitable_labels)
    if wrong_labels:
        logger.warning(
            f'Skipping {issue_id} due to labels {",".join(wrong_labels)}')
        return False

    if not set(label_names).intersection(gci_labels):
        logger.warning(f'Skipping {issue_id} due to missing gci labels')
        return False

    return True


def generate_task(issue, metadata):
    logger = logging.getLogger(__name__ + '.generate_task')

    title = issue.title
    title = title.replace('"', '').replace('!', '').replace('  ', ' ').strip()

    logger.info(f'generating task for issue {issue.number}: {title}')
    url = issue.web_url

    logger.debug(f'{url}: {title}')

    repo_name = metadata['repo_name']
    short_name = metadata['short_name']
    mentors = metadata.get('mentors')
    difficulty_level = metadata['difficulty_level']

    if 'tags' in metadata:
        tags = set(metadata['tags'])
    else:
        tags = set()

    tags.add('issues')

    # 1: Coding,
    # 2: User Interface,
    # 3: Documentation & Training,
    # 4: Quality Assurance
    # 5: Outreach & Research
    if repo_name in ['documentation', 'cEPs']:
        categories = [3]
    else:
        categories = [1]

    label_names = issue.labels

    logger.info(f'labels {",".join(label_names)}')

    if 'UI' in tags:
        tags.remove('UI')
        categories.append(2)
    if 'documentation' in tags:
        tags.remove('documentation')
        categories = [3]
    if 'documentation' in label_names or 'area/documentation' in label_names:
        categories = [3]
    if 'area/tests' in label_names:
        categories.append(4)
        tags |= {'pytest', 'unittest', 'unit test', 'unit tests'}

    if 'hoster/gitlab' in label_names:
        tags |= {'gitlab'}
    elif 'hoster/github' in label_names:
        tags |= {'github'}
    if '.coafile' in title:
        tags |= {'.coafile'}

    if difficulty_level == 'newcomer':
        if metadata['host']:
            tags.add('GitLab')
        else:
            tags.add('git')

    if 'README.md' in title:
        tags.add('markdown')
        assert difficulty_level == 'newcomer'
    elif '.md' in title:
        tags.add('markdown')
    elif '.rst' in title:
        tags.add('reStructuredText')
    elif 'newcomer' in title.lower():
        tags.add('reStructuredText')
    elif 'docstring' in title.lower():
        tags.add('reStructuredText')
        tags.add('python3')
        tags.add('docstring')

    if repo_name == 'corobo' and difficulty_level == 'newcomer':
        if 'type/markdown' in label_names or 'help' in title:
            tags.add('markdown')
        elif 'emoji' in title or 'shipit' in title or 'ship it' in title:
            tags.add('emoji')
        elif 'spelling' in title or issue in [426]:
            pass
        elif 3 in categories:  # documentation task
            pass
        else:
            logger.warning(
                f'Issue corobo {issue.id} doesnt look like a newcomer issue')
            return False
    elif repo_name == 'corobo':
        if 'type/regex' in label_names:
            tags.add('regex')
    elif repo_name == 'documentation' and difficulty_level == 'newcomer':
        if 'type/markdown' in label_names:
            tags.add('markdown')
        else:
            tags.add('reStructuredText')
    elif repo_name == 'cEPs':
        tags.add('markdown')
    elif repo_name == 'projects' and difficulty_level == 'newcomer':
        tags.add('markdown')

    if repo_name == 'corobo':
        if len(tags) <= 4:
            tags.add('errbot')
        if len(tags) <= 4:
            tags.add('chatops')
    elif repo_name == 'community':
        if len(tags) <= 4:
            tags.add('frontend')
        if len(tags) <= 4:
            tags.add('django')
        if len(tags) <= 4:
            tags.add('community')
    elif repo_name == 'dependency_management':
        if len(tags) <= 4:
            tags.add('packaging')
    elif repo_name == 'igitt':
        if len(tags) <= 4:
            tags.add('gitlab')
        if len(tags) <= 4:
            tags.add('api')
        if len(tags) <= 4:
            tags.add('webservices')
    elif repo_name in ('gci-leaders', 'gh-board'):
        if repo_name in ['gh-board'] and len(tags) <= 4:
            tags.add('React')

        if len(tags) <= 4:
            tags.add('Node')
        if len(tags) <= 4:
            tags.add('JavaScript')

    if 1 in categories and (
            'JavaScript' not in tags and 'javascript' not in tags):
        if len(tags) <= 4:
            tags.add('python3')

    logger.info(f'tags {",".join(tags)}')

    if 'markdown' in tags or 'reStructuredText' in tags:
        assert difficulty_level in ('newcomer', 'low')

    # time_to_complete_in_days must be between 3 and 7
    if difficulty_level in ('newcomer', 'low'):
        days = 3
    elif difficulty_level == 'medium':
        days = 4
    elif difficulty_level == 'high':
        days = 5
    elif difficulty_level == 'extreme':
        days = 7

    difficulty_label = metadata.get('difficulty_label', False)
    if difficulty_label:
        difficulty_label = difficulty_label.format(
            difficulty_level=difficulty_level)
        if difficulty_label not in label_names:
            logger.warning('incorrect difficult label')
            return False

    # TODO: resolve sub-component mentors
    if isinstance(mentors, dict):
        mentors = mentors['*']

    status = 1  # 1: draft, 2: published

    issue_id = issue.number

    task_name = f'{short_name}: Issue #{issue_id}: {title}'

    template = metadata['template']
    description = template.format(**locals())

    # max_instances is set to 2, even for issues with high numbers of instances
    # e.g. 26 for package_manager #127
    # This is to avoid many students overlapping on the same task.
    # TODO: Load the completed tasks instances, and incrementally increase
    # the total instance count until the limit for the issue.
    total_instances = metadata.get('instances', 1)
    if total_instances > 1:
        total_instances = 2

    task = {
        'name': task_name,
        'description': description,
        'status': status,
        'max_instances': total_instances,
        'mentors': mentors or [],
        'tags': list(tags),
        'is_beginner': difficulty_level == 'newcomer',
        'categories': categories,
        'time_to_complete_in_days': days,
        'external_url': url,
        'private_metadata': 'issues',
    }
    check_task(task)
    return task


def check_task(task):
    url = task['external_url']
    tags = task['tags']
    categories = task['categories']

    logger = logging.getLogger(__name__ + '.check_task')

    if not tags:
        logger.warning(f'task {url}: no tags')

    if not len(tags) <= MAX_TAGS:
        logger.warning(f'task {url}: too many tags: {",".join(tags)}')
        return False

    if 3 in categories:
        if ('markdown' not in tags and
                'reStructuredText' not in tags and
                '.coafile' in tags):
            logger.warning(
                f'task {url}: incorrect cat 3 tags: {",".join(tags)}')
            return False

    return True


def split_tags(tags):
    if isinstance(tags, list):
        return set(tags)
    return set(item.strip() for item in tags.split(','))


def get_issues(issues_list, metadata):
    """
    Handle a issue list data structure.

    :param issue_list: A dictionary of issue identifers with metadata.
    """
    logger = logging.getLogger(__name__ + '.get_issues')
    repo_name = metadata['repo_name']
    host = metadata['host']
    logger.info(f'processing repo {repo_name}')

    for issue_id, issue_metadata in issues_list.items():

        logger.debug(f'processing {issue_id}')

        if '/' in repo_name:
            url = f'https://{host}/{repo_name}/issues/{issue_id}'
        else:
            url = f'https://{host}/{org_name}/{repo_name}/issues/{issue_id}'

        logger.debug(f'url = {url}')

        all_metadata = metadata.copy()

        all_metadata['url'] = url

        old_tags = all_metadata.get('tags')
        new_tags = None
        if isinstance(issue_metadata, str):
            new_tags = issue_metadata
        if isinstance(issue_metadata, dict):
            new_tags = issue_metadata.get('tags')
            all_metadata.update(issue_metadata)
        elif isinstance(issue_metadata, list):
            new_tags = issue_metadata

        if new_tags:
            new_tags = split_tags(new_tags)

        if old_tags:
            old_tags = split_tags(old_tags)
            new_tags = old_tags.union(new_tags)

        if new_tags:
            all_metadata['tags'] = new_tags

        if all_metadata.get('disabled') is True:
            continue

        yield all_metadata


def load_issues(issues_list, metadata, available_only=False):
    logger = logging.getLogger(__name__ + '.load_issues')
    repo_name = metadata['repo_name']
    logger.info(f'processing repo {repo_name}')

    for issue_metadata in get_issues(issues_list, metadata):
        url = issue_metadata['url']
        logger.debug(f'url = {url}')

        issue = get_issue(url)
        assert issue

        if available_only:
            if not issue_is_available(issue):
                continue

        yield issue, issue_metadata


def _exclude_difficulty_levels(data):
    return dict([(name, item) for name, item in data.items()
                 if name not in difficulty_level_names])


def get_all_issues(issue_config, available_only=False):
    """
    Handle all project data structures.

    :param issue_config: Issue metadata for GCI tasks.
    """
    logger = logging.getLogger(__name__ + '.get_all_issues')

    global_metadata = issue_config['global']
    base_metadata = _exclude_difficulty_levels(global_metadata)

    for repo_name, data in issue_config.items():
        # meta key for templates, etc
        if repo_name == 'global':
            continue

        # A hack to allow skipping repos, e.g. already processed.
        if repo_name.startswith('#'):
            continue

        levels = dict([(name, item) for name, item in data.items()
                       if name in difficulty_level_names])

        repo_metadata = _exclude_difficulty_levels(data)

        if repo_metadata.get('disabled') is True:
            continue

        gitlab_repo_id = repo_metadata.get('gitlab_id')
        if gitlab_repo_id:
            repo_metadata['host'] = 'gitlab.com'
        else:
            repo_metadata['host'] = 'github.com'

        repo_metadata['repo_name'] = repo_name

        short_name = repo_metadata.get('short_name')
        if not short_name:
            short_name = repo_name.split('/')[-1]
            short_name = short_name.replace('_', ' ')
            short_name = short_name.replace(org_name + '-', '')
            repo_metadata['short_name'] = short_name

        logger.info(f'processing {short_name}')

        for difficulty_level, issues_list in levels.items():
            if difficulty_level.startswith('#'):
                continue

            issue_list_metadata = base_metadata.copy()
            issue_list_metadata['difficulty_level'] = difficulty_level
            issue_list_metadata.update(repo_metadata)
            if difficulty_level in global_metadata:
                issue_list_metadata.update(global_metadata[difficulty_level])
            if difficulty_level in repo_metadata:
                issue_list_metadata.update(repo_metadata[difficulty_level])

            yield from get_issues(issues_list, issue_list_metadata)


def get_issue_tasks(issue_config, available_only=True):
    logger = logging.getLogger(__name__ + '.get_issue_tasks')

    for issue_metadata in get_all_issues(issue_config):
        url = issue_metadata['url']
        logger.debug(f'url = {url}')
        issue = get_issue(url)
        assert issue

        if available_only:
            if not issue_is_available(issue):
                continue

        task = generate_task(issue, issue_metadata)

        if task:
            yield task


def print_tasks(tasks):
    for task in tasks:
        url = task['external_url']
        pprint.pprint(task)
        if not check_task(task):
            print(f'task check failed: {url}')


def upload_tasks(tasks, ask, publish):
    client = GCIAPIClient(get_api_key('GCI'))

    for task in tasks:
        url = task['external_url']

        if publish:
            task['publish'] = 2
        if not check_task(task):
            print(f'task check failed: {url}')
            continue

        existing_task = lookup_url(url, private=True)
        if existing_task:
            task_id = existing_task['id']
            print(f'task {task_id} is {url}')
            continue

        if ask:
            pprint.pprint(task)
            answer = input('Create task (y/n): ')
            if answer != 'y':
                continue

        client.NewTask(task)
        print('Task created.')
