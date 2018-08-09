import requests_mock

from django.test import TestCase

from data.merge_requests import fetch_mrs


class FetchMergeRequestTest(TestCase):

    def test_fetch_mrs(self):
        with requests_mock.Mocker():
            fetch_mrs('GitHub')
