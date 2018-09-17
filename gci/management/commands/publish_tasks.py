from django.core.management.base import BaseCommand

from gci.api_actions import publish_tasks
from gci.config import load_yaml
from gci.task import get_tasks


class Command(BaseCommand):
    help = 'Publish GCI tasks'

    def add_arguments(self, parser):
        parser.add_argument('filename')
        parser.add_argument('--repo')
        parser.add_argument('--mentors')

    def handle(self, *args, **options):
        filename = options.get('filename')
        mentor_config_filename = options.get('mentors')
        repo = options.get('repo')

        issue_config = load_yaml(filename)

        if repo:
            issue_config = dict((key, data)
                                for (key, data) in issue_config.items()
                                if key == 'global' or repo in key)

        tasks = get_tasks(private=True)

        publish_tasks(tasks, issue_config, mentor_config_filename)
