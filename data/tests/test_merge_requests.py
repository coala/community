import requests_mock

from django.test import TestCase

from data.merge_requests import fetch_mrs, import_mr
from gamification.tests.test_management_commands import (get_false_mrs_data)


class FetchMergeRequestTest(TestCase):

    def test_fetch_mrs(self):
        with requests_mock.Mocker():
            fetch_mrs('GitHub')

    def test_false_mr_data(self):
        for mr in get_false_mrs_data():
            import_mr('github', mr)
