import argparse

import giturlparse
from termcolor import colored
from django.core.management.base import BaseCommand

from gci.linter_repos import fetch_issues


class Command(BaseCommand):
    help = 'Fetch issues from linter repositories and filter'

    DEFAULT_LABELS = [
        'easy',
        'easy fix',
        'first issue',
        'good first issue',
        'newcomer',
        'help wanted',
        'beginner',
        'up-for-grabs',
        'beginner-friendly',
        'low-hanging fruit',
        'hacktoberfest',
    ]

    DEFAULT_KEYWORDS = [
        'easy fix',
        'documentation',
        'README',
        'pep8',
        'simple',
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--labels', '-l', nargs='*', default=Command.DEFAULT_LABELS)
        parser.add_argument(
            '--keywords', '-k', nargs='*', default=Command.DEFAULT_KEYWORDS)
        parser.add_argument('--processes', '-t', type=int)
        parser.add_argument('--all', action='store_true')
        parser.add_argument(
          'targets', type=argparse.FileType(),
          help='file containing tagret repositories')

    def handle(self, *args, **options):
        with options.get('targets') as targets_file:
            targets = targets_file.read().splitlines()

        results = fetch_issues(targets,
                               labels=options['labels'],
                               desc_keywords=options['keywords'],
                               processes=options.get('processes'),
                               debug=True)

        for _, sub in results.items():
            print_scope = 'all' if options.get('all') else 'filtered'

            for issue in sub[print_scope]:
                url = issue['repo_url']
                parsed_url = giturlparse.parse(url)

                issue_labels = str(issue['labels'])
                if not options.get('no_color'):
                    issue_labels = colored(issue_labels, 'cyan')

                print('{repo}#{id}: {labels} {title} '.format(
                  repo=parsed_url.pathname[1:],
                  id=issue['id'],
                  title=issue['title'],
                  labels=issue_labels))
