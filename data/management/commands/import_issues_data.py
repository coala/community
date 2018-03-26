from django.core.management.base import BaseCommand

from data.issues import fetch_issues, import_issue


class Command(BaseCommand):
    help = 'Import issues opened by newcomers'

    def handle(self, *args, **options):
        github_data = fetch_issues('GitHub')
        gitlab_data = fetch_issues('GitLab')
        if github_data:
            for data in github_data:
                import_issue('GitHub', data)
        if gitlab_data:
            for data in gitlab_data:
                import_issue('GitLab', data)
