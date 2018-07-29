import unittest

from django.core.management import call_command
from django.test import TestCase

from openhub.models import PortfolioProject
from community.git import get_org_name


class ImportPortfolioProjectDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('import_portfolio_projects_data')

    def test_command_import_portfolio_projects_data(self):
        org_name = get_org_name()
        p_projects = PortfolioProject.objects.all()
        if not p_projects:
            raise unittest.SkipTest(
                'No record of portfolio projects from openhub')
        self.assertIn(org_name,
                      [p_project.name for p_project in p_projects])
