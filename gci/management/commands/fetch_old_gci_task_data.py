import requests

from django.core.management.base import BaseCommand

from community.git import get_deploy_url


class Command(BaseCommand):
    help = 'Fetch old GCI data'

    def add_arguments(self, parser):
        parser.add_argument('output_dir', nargs='?', type=str)

    def handle(self, *args, **options):
        output_dir = options.get('output_dir')

        deploy_url = get_deploy_url()

        r = requests.get(deploy_url + '/static/tasks.yaml')
        r.raise_for_status()

        with open(os.path.join(output_dir, 'tasks.yaml'), 'w') as f:
            yaml.dump(r.content, f)

        r = requests.get(deploy_url + '/static/instances.yaml')
        r.raise_for_status()

        with open(os.path.join(output_dir, 'instances.yaml'), 'w') as f:
            yaml.dump(r.content, f)
