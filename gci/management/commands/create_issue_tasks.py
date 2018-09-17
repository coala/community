import pprint

from django.core.management.base import BaseCommand

from gci.api_actions import upload_tasks
from gci.config import load_yaml
from gci.issues import get_all_issues
from gci.issues import get_issue_tasks
from gci.issues import print_tasks


class Command(BaseCommand):
    help = 'Create GCI tasks from issues'

    def add_arguments(self, parser):
        parser.add_argument('filename')
        parser.add_argument('--mentors')
        parser.add_argument('--repo')
        parser.add_argument('-r', '--raw', dest='raw',
                            action='store_true', default=False)
        parser.add_argument('-a', '--ask', dest='ask',
                            action='store_true', default=False)
        parser.add_argument('-f', '--force', dest='force',
                            action='store_true', default=False)
        parser.add_argument('-p', '--publish', dest='publish',
                            action='store_true', default=False)

    def handle(self, *args, **options):
        filename = options.get('filename')
        mentor_config_filename = options.get('mentors')
        repo = options.get('repo')
        raw = options.get('raw')
        ask = options.get('ask')

        issue_config = load_yaml(filename)

        if repo:
            issue_config = dict((key, data)
                                for (key, data) in issue_config.items()
                                if key == 'global' or repo in key)

        if raw:
            issues = list(get_all_issues(issue_config))
            pprint.pprint(issues)
            return

        tasks = get_issue_tasks(issue_config, available_only=True)

        if ask:
            upload_tasks(tasks, mentor_config_filename)
        else:
            print('Dry run, printing task below.')
            print_tasks(tasks)

            print("""
No tasks uploaded. Add a -f argument to upload tasks to the GCI website.
""")
