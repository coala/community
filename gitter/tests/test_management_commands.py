from django.test import TestCase
from django.core.management import call_command

from gitter.models import Message


class ImportContributorDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('import_messages_data')

    def test_command_import_contributors_data(self):
        messages = Message.objects.all()
        self.assertIn('testuser',
                      [message.sent_by for message in messages])
