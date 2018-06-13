import unittest

from django.core.management import call_command
from django.test import TestCase

from openhub.models import OutsideProject


class ImportOutsideProjectDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('import_outside_projects_data')

    def test_command_import_outside_projects_data(self):
        o_projects = OutsideProject.objects.all()
        if not o_projects:
            raise unittest.SkipTest(
                'No record of outside projects from openhub')
        self.assertIn('dependency_management',
                      [o_project.name for o_project in o_projects])
