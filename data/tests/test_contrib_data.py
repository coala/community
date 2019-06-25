import requests_mock

from django.test import TestCase

from data.contrib_data import get_contrib_data, import_data
from gamification.tests.test_management_commands import (
    get_false_contributors_data)


class GetContribDataTest(TestCase):

    def test_get_contrib_data(self):
        with requests_mock.Mocker():
            get_contrib_data()

    def test_false_contributor_data(self):
        for contrib in get_false_contributors_data():
            import_data(contrib)
