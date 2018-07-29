import unittest

from django.core.management import call_command
from django.test import TestCase

from openhub.models import AffiliatedCommitter


class ImportAffiliatedCommitterDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('import_affiliated_committers_data')

    def test_command_import_affiliated_committers_data(self):
        a_committers = AffiliatedCommitter.objects.all()
        if not a_committers:
            raise unittest.SkipTest(
                'No record of affiliated committers from openhub')
        self.assertIn('John Vandenberg',
                      [a_committer.name for a_committer in a_committers])
