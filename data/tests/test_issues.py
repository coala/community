import requests_mock

from django.test import TestCase

from data.issues import fetch_issues, import_issue
from gamification.tests.test_management_commands import (
    get_false_issues_data)


class FetchIssueTest(TestCase):

    def test_fetch_issues(self):
        with requests_mock.Mocker():
            fetch_issues('GitHub')

    def test_false_issue_data(self):
        for issue in get_false_issues_data():
            import_issue('github', issue)
