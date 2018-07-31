import requests_mock

from django.test import TestCase

from gitter.messages import get_messages


class GetMessagesTest(TestCase):

    def test_get_messages(self):
        with requests_mock.Mocker():
            get_messages()
