import logging
import pprint

from gci.gitorg import get_issue
from gci.task import lookup_url

from community.git import get_org_name

org_name = get_org_name()

unsuitable_labels = {
    'status/blocked',
    'status/invalid',
    'status/needs info',
    'status/needs design',
    'status/needs discussion',
}

difficulty_level_names = ('newcomer', 'low', 'medium', 'high', 'extreme')

MAX_TAGS = 5

# 1: 'Code',
# 2: Design (User Interface, Artwork, etc)
# 3: Documentation & Training
# 4: Quality Assurance
# 5: Outreach & Research

CATEGORY_TAGS = {
    'design': 2,
    'ui': 2,
    'UI': 2,
    'artwork': 2,
    'svg': 2,
    'docs': 3,
    'documentation': 3,
    'pdf': 3,
    'markdown': 3,
    'reStructuredText': 3,
    'training': 3,
    'video': 3,
    'unittest': 4,
    'tests': 4,
    'qa': 4,
    'outreach': 5,
    'research': 5,
}
# These tags will be removed after category allocation.
# i.e. they are unsuitable for GCI tags, as unlikely search terms,
# or duplicate the GCI category filter.
CATEGORY_ONLY_TAGS = [
    'design',
    'docs',
    'documentation',
    'training',
    'outreach',
    'research',
]


def issue_is_available(issue, issue_metadata):
    logger = logging.getLogger(__name__ + '.issue_is_available')

    issue_id = issue.number
    url = issue.web_url

    logger.debug(f'checking {issue_id} availability...')

    if str(issue.state) in ('closed', ):
        logger.info(f'{issue_id}: {issue.state}')
        return False

    if str(issue.state) not in ('open', ):
        logger.warning(f'{url}: Unexpected state {issue.state}')
        return False

    if issue.assignees:
        assignees = [assignee.username for assignee in issue.assignees]
        if len(assignees):
            assignees = assignees[0]
        logger.warning(f'Skipping {url} assigned to {assignees}')
        return False

    assert issue.title

    label_names = set(issue.labels)

    required_label = issue_metadata.get('required_label')
    if required_label and required_label not in label_names:
        logger.warning(
            f'Skipping {issue_id} due to missing label {required_label}')
        return False

    if label_names:
        wrong_labels = label_names.intersection(unsuitable_labels)
        if wrong_labels:
            logger.warning(
                f'Skipping {issue_id} due to labels {",".join(wrong_labels)}')
            return False

    logger.info(f'{issue_id} is available')

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

    tags = set(metadata.get('tags', []))

    tags.add('issues')

    if 'rst' in tags:
        tags.add('reStructuredText')
        tags.remove('rst')
    if 'restructuredtext' in tags:
        tags.add('reStructuredText')
        tags.remove('restructuredtext')

    label_names = issue.labels

    logger.info(f'labels {",".join(label_names)}')

    if 'documentation' in label_names or 'area/documentation' in label_names:
        tags.add('documentation')
    if 'area/tests' in label_names:
        tags |= {'pytest', 'unittest', 'unit test', 'unit tests'}

    if 'hoster/gitlab' in label_names:
        tags |= {'gitlab'}
    elif 'hoster/github' in label_names:
        tags |= {'github'}
    if '.coafile' in title:
        tags |= {'.coafile'}

    if difficulty_level == 'newcomer':
        if metadata['host'] == 'gitlab.com':
            tags.add('GitLab')
        else:
            tags.add('git')

    if 'README.md' in title:
        tags.add('markdown')
        assert difficulty_level == 'newcomer'
    elif '.md' in title:
        if 'reStructuredText' not in tags:
            tags.add('markdown')
    elif '.rst' in title:
        if 'markdown' not in tags:
            tags.add('reStructuredText')
    elif 'newcomer' in title.lower():
        # Newcomers guide
        tags.add('reStructuredText')
    elif 'docstring' in title.lower():
        tags.add('reStructuredText')
        tags.add('python3')
        tags.add('docstring')

    if repo_name.endswith('corobo') and difficulty_level == 'newcomer':
        if 'type/markdown' in label_names or 'help' in title:
            tags.add('markdown')
        elif 'emoji' in title or 'shipit' in title or 'ship it' in title:
            tags.add('emoji')
        elif 'spelling' in title or issue in [426]:
            pass
        elif 'documentation' in tags:  # documentation task
            pass
        else:
            logger.warning(
                f'Issue corobo {issue.id} doesnt look like a newcomer issue')
            return False
    elif repo_name.endswith('corobo'):
        if 'type/regex' in label_names:
            tags.add('regex')

    categories = set()
    for tag in list(tags):
        category = CATEGORY_TAGS.get(tag)
        if category:
            categories.add(category)
            if tag in CATEGORY_ONLY_TAGS:
                tags.remove(tag)

    # Default to Code
    if not categories:
        categories.add(1)

    if repo_name.endswith('corobo'):
        if len(tags) <= 4:
            tags.add('errbot')
        if len(tags) <= 4:
            tags.add('chatops')
    elif repo_name.endswith('community'):
        if len(tags) <= 4:
            tags.add('frontend')
        if len(tags) <= 4:
            tags.add('django')
        if len(tags) <= 4:
            tags.add('community')
    elif repo_name.lower().endswith('igitt'):
        if len(tags) <= 4:
            tags.add('gitlab')
        if len(tags) <= 4:
            tags.add('api')
        if len(tags) <= 4:
            tags.add('webservices')

    if 'React' in tags and len(tags) < 5:
        tags.add('Node')
        if len(tags) < 5:
            tags.add('JavaScript')

    if 1 in categories and (
            'JavaScript' not in tags and 'javascript' not in tags):
        if len(tags) <= 4:
            tags.add('python3')

    if 'python2' in tags and 'python3' in tags and len(tags) > 5:
        tags.remove('python2')

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
            logger.warning(f'{url}: missing {difficulty_label}')
            return False

    # TODO: resolve sub-component mentors
    if isinstance(mentors, dict):
        mentors = mentors['*']

    status = 1  # 1: draft, 2: published

    issue_id = issue.number

    name = f'{short_name}: Issue #{issue_id}: {title}'

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

    task_values = {
        'name': name,
        'description': description,
        'status': status,
        'max_instances': total_instances,
        'mentors': mentors or [],
        'tags': list(tags),
        'is_beginner': difficulty_level == 'newcomer',
        'categories': list(categories),
        'time_to_complete_in_days': days,
        'external_url': url,
        'private_metadata': 'issues',
    }
    check_task(task_values)
    return task_values


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
        if not isinstance(issue_id, int):
            logger.warning(f'skipping {issue_id}')
            continue

        if 'blocked' in metadata:
            if metadata['blocked'] != issue_id:
                logger.info(f'skipping blocked {repo_name} {issue_id}')
                continue

        logger.info(f'processing .. {repo_name} {issue_id}')

        url = f'https://{host}/{repo_name}/issues/{issue_id}'

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
            if new_tags:
                new_tags = old_tags.union(new_tags)
            else:
                new_tags = old_tags

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
            if not issue_is_available(issue, issue_metadata):
                continue

        yield issue, issue_metadata


def _exclude_difficulty_levels(data):
    return dict([(name, item) for name, item in data.items()
                 if name not in difficulty_level_names])


def get_projects(issue_config, yield_levels=True):
    """
    Normalise project data structures.

    :param issue_config: Issue metadata for GCI tasks.
    """
    logger = logging.getLogger(__name__ + '.get_projects')

    for key, data in issue_config.items():
        # meta key for templates, etc
        if key == 'global':
            continue

        assert key == key.lower(), f'key {key} should be lowercase'

        # A hack to allow skipping repos, e.g. already processed.
        if key.startswith('#'):
            continue
        if not data:
            continue

        logger.warning(f'processing {key}')

        repo_metadata = _exclude_difficulty_levels(data)

        if repo_metadata.get('disabled') is True:
            continue

        if 'repo_name' in repo_metadata:
            repo_name = repo_metadata['repo_name']
        elif '/' in key:
            repo_name = key
            repo_org = key.split('/', 1)[0]
        else:
            repo_org = org_name
            repo_name = f'{org_name}/{key}'
            key = repo_name
        repo_metadata['repo_org'] = repo_org

        if ':' in repo_name:
            repo_name = repo_name.split(':', 1)[0]
        repo_metadata['repo_name'] = repo_name

        gitlab_repo_id = repo_metadata.get('gitlab_id')
        if gitlab_repo_id:
            repo_metadata['host'] = 'gitlab.com'
        else:
            repo_metadata['host'] = 'github.com'

        short_name = repo_metadata.get('short_name')
        if not short_name:
            short_name = repo_name.split('/')[-1]
            short_name = short_name.replace('_', ' ')
            short_name = short_name.replace(org_name + '-', '')
            repo_metadata['short_name'] = short_name

        if yield_levels:
            levels = dict([(name, item)
                           for name, item in data.items()
                           if name in difficulty_level_names])

            yield key, repo_metadata, levels
        else:
            yield key, repo_metadata


def get_all_issues(issue_config, available_only=False):
    """
    Convert projects data structure into items for each issue.

    :param issue_config: Issue metadata for GCI tasks.
    """
    logger = logging.getLogger(__name__ + '.get_all_issues')

    global_metadata = issue_config['global']

    base_metadata = _exclude_difficulty_levels(global_metadata)

    for key, project_metadata, levels in get_projects(issue_config):
        repo_org = project_metadata['repo_org']

        logger.info(f'processing {key}')

        for difficulty_level, issues_list in levels.items():
            if difficulty_level.startswith('#'):
                continue

            issue_list_metadata = base_metadata.copy()

            if repo_org in global_metadata:
                issue_list_metadata.update(global_metadata[repo_org])

            issue_list_metadata['difficulty_level'] = difficulty_level
            issue_list_metadata.update(project_metadata)

            if difficulty_level in global_metadata:
                issue_list_metadata.update(global_metadata[difficulty_level])
            if difficulty_level in project_metadata:
                issue_list_metadata.update(project_metadata[difficulty_level])

            logger.warning(f'processing .. {key} {difficulty_level}')

            yield from get_issues(issues_list, issue_list_metadata)


def get_issue_tasks(issue_config, available_only=True):
    logger = logging.getLogger(__name__ + '.get_issue_tasks')

    for issue_metadata in get_all_issues(issue_config):
        url = issue_metadata['url']
        logger.debug(f'url = {url}')
        issue = get_issue(url)
        assert issue

        if available_only:
            if not issue_is_available(issue, issue_metadata):
                continue

        task = generate_task(issue, issue_metadata)

        if task:
            yield task


def print_tasks(tasks):
    logger = logging.getLogger(__name__ + '.print_tasks')
    for task in tasks:
        url = task['external_url']

        existing_task = lookup_url(url, private=True)
        if existing_task:
            task_id = existing_task['id']
            logger.warning(f'{url} is task {task_id}')
            continue

        pprint.pprint(task)

        if not check_task(task):
            logger.warning(f'task check failed: {url}')
