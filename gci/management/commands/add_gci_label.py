import logging

# Start ignoring KeywordBear
from coala_utils.Question import ask_yes_no
# Stop ignoring

from django.core.management.base import BaseCommand

from gci.config import load_yaml
from gci.gitorg import get_issue
from gci.issues import filter_issue_config
from gci.issues import get_all_issues
from gci.issues import issue_is_available


class Command(BaseCommand):
    help = 'Add GCI label to issues'

    def add_arguments(self, parser):
        parser.add_argument('filename')
        parser.add_argument('--repo')
        parser.add_argument('-f', '--force', dest='force',
                            action='store_true', default=False)

    def handle(self, *args, **options):
        filename = options.get('filename')
        repo = options.get('repo')
        force = options.get('force')

        logger = logging.getLogger(__name__ + '.handle')

        issue_config = load_yaml(filename)

        if repo:
            issue_config = filter_issue_config(issue_config, repo)

        for issue_metadata in get_all_issues(issue_config):
            required_label = issue_metadata.get('required_label')
            if not required_label:
                continue
            url = issue_metadata['url']
            logger.debug(f'url = {url}')
            issue = get_issue(url)
            if not issue_is_available(issue, issue_metadata,
                                      ignore_required_label=True):
                continue
            if required_label in issue.labels:
                continue
            title = issue.title
            print(f'Label {required_label} missing on {url} {title}')
            if not force and not ask_yes_no(f'Add label', 'no'):
                continue
            try:
                issue.labels |= set([required_label])
            except Exception as e:
                print(f'Failed {e}')
