import unittest

from django.core.management import call_command
from django.test import TestCase

from openhub.models import OutsideCommitter


class ImportOutsideCommitterDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('import_outside_committers_data')

    def test_command_import_outside_committers_data(self):
        o_committers = OutsideCommitter.objects.all()
        if not o_committers:
            raise unittest.SkipTest(
                'No record of outside committers from openhub')
        self.assertIn('satwikkansal',
                      [o_committer.name for o_committer in o_committers])
