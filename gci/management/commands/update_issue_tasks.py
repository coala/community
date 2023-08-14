from django.core.management.base import BaseCommand

from gci.api_actions import update_issue_tasks
from gci.config import load_yaml
from gci.issues import filter_issue_config
from gci.task import get_tasks


class Command(BaseCommand):
    help = 'Update GCI tasks'

    def add_arguments(self, parser):
        parser.add_argument('filename', help='Path to issues.yaml')
        parser.add_argument('--mentors', help='Path to mentors.yaml')
        parser.add_argument('--repo', help='Repo filter')
        parser.add_argument('--all', help='Include unavailable issues',
                            action='store_true', default=False)

    def handle(self, *args, **options):
        filename = options.get('filename')
        mentor_config_filename = options.get('mentors')
        repo = options.get('repo')
        all_tasks = options.get('all')

        issue_config = load_yaml(filename)

        if repo:
            issue_config = filter_issue_config(issue_config, repo)

        tasks = get_tasks(private=True)

        update_issue_tasks(
            tasks, issue_config, mentor_config_filename,
            all_tasks,
            )
