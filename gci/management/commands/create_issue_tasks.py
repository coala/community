import pprint

from django.core.management.base import BaseCommand

from gci.config import load_yaml
from gci.issues import get_all_issues
from gci.issues import get_issue_tasks
from gci.issues import print_tasks
from gci.issues import upload_tasks


class Command(BaseCommand):
    help = 'Create GCI tasks from issues'

    def add_arguments(self, parser):
        parser.add_argument('filename')
        parser.add_argument('-r', '--raw', dest='raw',
                            action='store_true', default=False)
        parser.add_argument('-a', '--ask', dest='ask',
                            action='store_true', default=False)
        parser.add_argument('-f', '--force', dest='force',
                            action='store_true', default=False)
        parser.add_argument('-p', '--publish', dest='publish',
                            action='store_true', default=False)
        parser.add_argument('output_dir', nargs='?', type=str)

    def handle(self, *args, **options):
        filename = options.get('filename')
        raw = options.get('raw')
        ask = options.get('ask')
        force = options.get('force')
        publish = options.get('publish')
        # Note it is not possible to auto-publish until mentors
        # are pre-allocated to tasks.
        force = options.get('force')

        issue_config = load_yaml(filename)

        if raw:
            issues = list(get_all_issues(issue_config))
            pprint.pprint(issues)
            return

        tasks = get_issue_tasks(issue_config, available_only=True)

        if ask or force:
            upload_tasks(tasks, ask, publish)
        else:
            print('Dry run, printing task below.')
            print_tasks(tasks)

            print("""
No tasks uploaded. Add a -f argument to upload tasks to the GCI website.
""")
