from django.test import TestCase

from data.models import Contributor
from data.org_cluster_map_handler import handle as org_cluster_map_handler


class CreateOrgClusterMapAndActivityGraphTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Contributor.objects.create(login='test',
                                   name='Test User',
                                   location='{"latitude": 12.9,'
                                            '"longitude": 77.8}')
        Contributor.objects.create(login='testuser',
                                   name='Test User 2')

    def test_with_output_dir(self):
        org_cluster_map_handler()

    def test_without_output_dir(self):
        org_cluster_map_handler(output_dir='org_map')
