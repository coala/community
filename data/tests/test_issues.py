import requests_mock

from django.test import TestCase

from data.issues import fetch_issues


class FetchIssueTest(TestCase):

    def test_fetch_issues(self):
        with requests_mock.Mocker():
            fetch_issues('GitHub')
