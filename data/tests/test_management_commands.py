import unittest

from django.core.management import call_command
from django.test import TestCase

from data.models import Contributor, Issue, MergeRequest


class ImportContributorDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('import_contributors_data')

    def test_command_import_contributors_data(self):
        contributors = Contributor.objects.all()
        if not contributors:
            raise unittest.SkipTest(
                'No record of contributors from webservices')
        self.assertIn('jayvdb',
                      [contributor.login for contributor in contributors])


class ImportIssuesDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('import_issues_data')

    def test_command_import_issues_data(self):
        issues = Issue.objects.all()
        if not issues:
            raise unittest.SkipTest(
                'No record of issues from webservices')
        self.assertIn('testuser',
                      [issue.author.login for issue in issues])


class ImportMergeRequestDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('import_merge_requests_data')

    def test_command_import_issues_data(self):
        mrs = MergeRequest.objects.all()
        if not mrs:
            raise unittest.SkipTest(
                'No record of mrs from webservices')
        self.assertIn('testuser',
                      [mr.author.login for mr in mrs])
