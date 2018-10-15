from collections import OrderedDict
import os.path

from ruamel.yaml import YAML

from django.core.management.base import BaseCommand

from gci.students import (
    _get_instances,
    _get_tasks,
)


class Command(BaseCommand):
    help = 'Fetch GCI data'

    def add_arguments(self, parser):
        parser.add_argument('output_dir', type=str)

    def handle(self, *args, **options):
        output_dir = options.get('output_dir')

        tasks = {}
        for task in _get_tasks():
            tasks[int(task['id'])] = task

        instances = {}
        for instance in _get_instances():
            instances[int(instance['id'])] = instance

        tasks = OrderedDict(sorted(tasks.items(), key=lambda t: t[0]))
        instances = OrderedDict(sorted(instances.items(), key=lambda t: t[0]))

        yaml = YAML()

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        with open(os.path.join(output_dir, 'tasks.yaml'), 'w') as f:
            yaml.dump(tasks, f)

        with open(os.path.join(output_dir, 'instances.yaml'), 'w') as f:
            yaml.dump(instances, f)
