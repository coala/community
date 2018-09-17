import argparse
import logging
import pprint
import sys

from .client import GCIAPIClient
from .config import get_api_key
from .gitorg import get_issue

from .issue_data import (
    coala_mentors,
    corobo_mentors,
    gitmate_mentors,
    pm_mentors,
    all_issues,
)

org_name = 'coala'

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


def issue_is_available(issue):
    logger = logging.getLogger(__name__ + '.issue_is_available')

    issue_id = issue.id

    if str(issue.state) in ('closed', ):
        logger.info('%d: %s' % (issue_id, issue.state))
        return False

    if str(issue.state) not in ('open', ):
        logger.warning('Wow , %d is in state %s' % (issue_id, issue.state))
        return False

    if issue.assignees:
        logger.warning('Skipping %d assigned to %s' % (issue_id, issue.assignees))
        return False

    logger.debug(pprint.pprint(issue))

    assert issue.title

    label_names = issue.labels

    wrong_labels = set(label_names).intersection(unsuitable_labels)
    if wrong_labels:
        logger.warning('Skipping %d due to labels %s' %
                       (issue_id, ','.join(wrong_labels)))
        return False

    if not set(label_names).intersection(gci_labels):
        logger.warning('Skipping %d due to missing gci labels' %
                       issue_id)
        return False

    return True


def generate_task(issue, metadata):
    logger = logging.getLogger(__name__ + '.generate_task')

    repo_name = metadata['repo_name']
    short_name = metadata['short_name']
    mentors = metadata['mentors']
    difficulty_level = metadata['difficulty_level']

    head_description = """Your task is to solve a '{}' difficulty issue in the
{} repository. Here is the issue:

""".format(difficulty_level, repo_name)

    if difficulty_level == 'newcomer':
        tail_description = """

Read [Git Basics](http://coala.io/git) and [Newcomer Guide](http://coala.io/newcomer)
to learn how to prepare your patch properly.
"""
    else:
        tail_description = """

Remember to format your [Git Commit Message](http://coala.io/commit)
according to the rules, otherwise the bot will tell you to fix it.
"""

    label_names = issue.labels

    title = issue.title

    logger.info('%d labels %s' % ','.join(label_names))

    if metadata['tags']:
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

    if '.md' in title:
        tags.add('markdown')
    if '.rst' in title:
        tags.add('reStructuredText')
    if 'newcomers' in title.lower():
        tags.add('reStructuredText')
    if 'docstring' in title.lower():
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
            logger.warning('Issue corobo %d doesnt look like a newcomer issue' % issue.id)
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
    elif repo_name == 'coala' and difficulty_level == 'newcomer':
        if 'markdown' not in tags:
            tags.add('reStructuredText')

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

    if 1 in categories and 'JavaScript' not in tags and 'javascript' not in tags:
        if len(tags) <= 4:
            tags.add('python3')

    logger.info('%d tags %s' % ','.join(tags))

    description = 'Issue [#{0}]({1}) {2}'.format(issue, issue.url, title)

    # time_to_complete_in_days must be between 3 and 7
    if difficulty_level in ('newcomer', 'low'):
        days = 3
    elif difficulty_level == 'medium':
        days = 4
    elif difficulty_level == 'high':
        days = 5
    elif difficulty_level == 'extreme':
        days = 7

    # currently only checking coala org
    # need to apply to other orgs with different labels, esp newcomer
    if '/' not in repo_name:
        if 'difficulty/%s' % difficulty_level not in label_names:
            logger.warning('incorrect difficult label')
            return False

    # TODO: resolve subcomponent mentors
    if isinstance(mentors, dict):
        mentors = mentors['*']

    status = 1  # 1: draft, 2: published

    task = {
        'name': '{short_name}: Issue #{issue_id} {title}'.format(
            short_name=short_name,
            issue_id=issue,
            title=title).replace('"', '').replace('!', ''),
        'description': head_description + description + tail_description,
        'status': status,
        'max_instances': 1,
        'mentors': mentors,
        'tags': list(tags),
        'is_beginner': difficulty_level == 'newcomer',
        'categories': categories,
        'time_to_complete_in_days': days,
        'external_url': issue.url,
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
        logger.warning('task %s: no tags' % url)

    if not len(tags) <= 5:
        logger.warning('task %s: too many tags: %s' % (url, ','.join(tags)))
        return False

    if 3 in categories:
        if ('markdown' not in tags and
                'reStructuredText' not in tags and
                '.coafile' in tags):
            logger.warning('task %s: incorrect cat 3 tags: %s' %
                           (url, ','.join(tags)))
            return False

    return True


def get_issues(issues_list, metadata):
    """Handle a issue list data structure."""
    logger = logging.getLogger(__name__ + '.get_issues')
    repo_name = metadata['repo_name']
    host = metadata['host']
    logger.info('processing repo %s' % repo_name)

    for issue_id, issue_metadata in issues_list.items():

        logger.debug('processing %d' % issue_id)

        if '/' in repo_name:
            url = "https://{host}/{repo_name}/issues/{issue_id}".format(
                host=host,
                repo_name=repo_name,
                issue_id=str(issue_id),
            )
        else:
            url = "https://{host}/{org_name}/{repo_name}/issues/{issue_id}".format(
                host=host,
                org_name=org_name,
                repo_name=repo_name,
                issue_id=str(issue_id),
            )

        logger.debug('url = %s' % url)

        all_metadata = metadata.copy()

        all_metadata['url'] = url

        if isinstance(issue_metadata, dict):
            all_metadata.update(issue_metadata)
        elif isinstance(issue_metadata, (set, list)):
            if 'tags' in all_metadata:
                for tag in issue_metadata:
                    all_metadata['tags'].add(tag)
            else:
                all_metadata['tags'] = set(issue_metadata)

        yield all_metadata


def load_issues(issues_list, metadata, available_only=False):
    logger = logging.getLogger(__name__ + '.load_issues')
    repo_name = metadata['repo_name']
    logger.info('processing repo %s' % repo_name)

    for issue_metadata in get_issues(issues_list, metadata):
        url = metadata['url']
        logger.debug('url = %s' % url)

        issue = get_issue(url)
        assert issue

        if available_only:
            if not issue_is_available(issue):
                continue

        yield issue, issue_metadata


def get_all_issues(available_only=False):
    """
    Handle all project data structures.
    :param raw: Do not load the issues
    """
    logger = logging.getLogger(__name__ + '.get_all_issues')

    for repo_name, data in all_issues.items():
        # A hack to allow skipping repos, e.g. already processed.
        if repo_name.startswith('#'):
            continue

        levels = dict([(name, item) for name, item in data.items()
                       if name in difficulty_level_names])

        metadata = dict([(name, item) for name, item in data.items()
                         if name not in difficulty_level_names])

        gitlab_repo_id = metadata.get('gitlab_id')
        if gitlab_repo_id:
            metadata['host'] = 'gitlab.com'
        else:
            metadata['host'] = 'github.com'

        metadata['repo_name'] = repo_name
        short_name = data.get('short_name')
        if not short_name:
            short_name = repo_name.split('/')[-1]
            short_name = short_name.replace('_', ' ').replace('coala-', '')
        metadata['short_name'] = short_name

        logger.info('processing %s' % metadata['short_name'])

        for difficulty_level, issues_list in levels.items():
            if difficulty_level.startswith('#'):
                continue

            metadata['difficulty_level'] = difficulty_level

            yield from get_issues(issues_list, metadata)


def get_issue_tasks(available_only=True):

    for issue_metadata in get_all_issues():
        url = issue_metadata['url']
        logger.debug('url = %s' % url)
        issue = get_issue(url)
        assert issue

        if available_only:
            if not issue_is_available(issue):
                continue

        task = generate_task(issue, issue_metadata)

        if task:
            yield task


def print_tasks(tasks):
    print("Dry run, printing task below.")
    for task in tasks:
        pprint.pprint(task)
        if not check_task(task):
            print('task check failed: %s' % task['external_url'])


def upload_tasks(tasks, publish):
    client = GCIAPIClient(get_api_key('GCI'))

    for task in tasks:
        if publish:
            task['publish'] = 2
        if not check_task(task):
            print('task check failed: %s' % task['external_url'])
        else:
            client.create_new_task(task)
            print("Task created.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--raw', dest='raw', action="store_true", default=False)
    parser.add_argument('-f', '--force', dest='force', action="store_true", default=False)
    parser.add_argument('-p', '--publish', dest='publish', action="store_true", default=False)
    args = parser.parse_args()

    if args.raw:
        issues = list(get_all_issues())
        pprint.pprint(issues)
        return

    tasks = get_issue_tasks(available_only=True)

    if args.force:
        upload_tasks(tasks, args.publish)
    else:
        print_tasks(tasks)

    if not args.force:
        print("""
No tasks uploaded. Add a -f argument to upload tasks to the GCI website.
This is not idempotent.
Running this twice with -f will create two sets of tasks.
""")
