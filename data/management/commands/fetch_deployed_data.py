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
        parser.add_argument('--repo-name', action='store',
                            dest='repo-name', type=str)
        parser.add_argument('--allow-failure', action='store_true',
                            dest='allow-failure', default=False,
                            help='Don\'t raise exceptions.')

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        output_dir = options.get('output_dir')
        filenames = options.get('filenames')
        repo_name = options.get('repo-name')
        allow_failure = options.get('allow-failure')

        deploy_url = get_deploy_url(repo_name)
        try:
            upstream_deploy_url = get_upstream_deploy_url(repo_name)
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
                    if not allow_failure:
                        r.raise_for_status()
                else:
                    if allow_failure:
                        return
                    else:
                        raise

            filename = os.path.basename(filename)
            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(r.content)
