import logging
import os.path

import requests

from django.core.management.base import BaseCommand

from community.git import get_deploy_url, get_upstream_deploy_url


class Command(BaseCommand):
    help = 'Fetch old data'

    def add_arguments(self, parser):
        parser.add_argument('output_dir', nargs='?', type=str)
        parser.add_argument('filenames', nargs='+', type=str)

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        output_dir = options.get('output_dir')
        filenames = options.get('filenames')

        deploy_url = get_deploy_url()
        try:
            upstream_deploy_url = get_upstream_deploy_url()
        except RuntimeError as e:
            upstream_deploy_url = None
            logger.info(str(e))

        for filename in filenames:
            r = requests.get(deploy_url + '/' + filename)
            try:
                r.raise_for_status()
            except Exception:
                if upstream_deploy_url:
                    r = requests.get(upstream_deploy_url + '/' + filename)
                    r.raise_for_status()
                else:
                    raise

            filename = os.path.basename(filename)
            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(r.content)
