import unittest

from community.git import get_config_remote
from community.git import get_deploy_url
from community.git import get_org_name
from community.git import get_remote_url


class GitTestCase(unittest.TestCase):

    def test_config_remote(self):
        remote = get_config_remote()
        self.assertEqual('url', remote[0][0])
        self.assertIn('/community', remote[0][1])

    def test_remote_url(self):
        url = get_remote_url()
        self.assertIn('/community', url.pathname)
        self.assertEqual('community', url.name)
        self.assertIn(url.resource, ['gitlab.com', 'github.com'])

    def test_org_name(self):
        org_name = get_org_name()
        self.assertTrue(org_name)

    def test_deploy_url(self):
        url = get_deploy_url()
        self.assertIn('/community', url)
