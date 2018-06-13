from django.core.management import call_command
from django.test import TestCase

from openhub.models import Organization
from community.git import get_org_name


class ImportOrganizationDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('import_organization_data')

    def test_command_import_organization_data(self):
        org_name = get_org_name()
        org = Organization.objects.get(name=org_name)
        self.assertIsNotNone(org)
