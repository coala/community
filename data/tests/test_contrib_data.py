import requests_mock

from django.test import TestCase

from data.contrib_data import get_contrib_data


class GetContribDataTest(TestCase):

    def test_get_contrib_data(self):
        with requests_mock.Mocker():
            get_contrib_data()
