from collections import OrderedDict
import os.path

from ruamel.yaml import YAML

from django.core.management.base import BaseCommand

from gci.students import (
    _get_instances,
    _get_tasks,
    cleanse_instances,
)
from gci.task import (
    cleanse_tasks,
)


class Command(BaseCommand):
    args = ''
    help = 'Cleanse GCI data'

    def add_arguments(self, parser):
        parser.add_argument('input_dir', nargs='?', type=str)
        parser.add_argument('output_dir', nargs='?', type=str)

    def handle(self, *args, **options):
        input_dir = options.get('input_dir')
        output_dir = options.get('output_dir')

        yaml = YAML()

        with open(os.path.join(input_dir, 'tasks.yaml'), 'r') as f:
            tasks = yaml.load(f)

        with open(os.path.join(input_dir, 'instances.yaml'), 'r') as f:
            instances = yaml.load(f)

        tasks = cleanse_tasks(tasks)
        instances = cleanse_instances(instances, tasks)

        with open(os.path.join(output_dir, 'tasks.yaml'), 'w') as f:
            yaml.dump(tasks, f)

        with open(os.path.join(output_dir, 'instances.yaml'), 'w') as f:
            yaml.dump(instances, f)
