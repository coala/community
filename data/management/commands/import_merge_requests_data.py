from django.core.management.base import BaseCommand

from data.merge_requests import fetch_mrs, import_mr


class Command(BaseCommand):
    help = 'Import mrs opened by newcomers'

    def handle(self, *args, **options):
        github_data = fetch_mrs('GitHub')
        gitlab_data = fetch_mrs('GitLab')
        if github_data:
            for data in github_data:
                import_mr('GitHub', data)
        if gitlab_data:
            for data in gitlab_data:
                import_mr('GitLab', data)
