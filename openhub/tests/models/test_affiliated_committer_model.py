from django.test import TestCase

from openhub.models import (
    AffiliatedCommitter,
    MostCommit,
    MostRecentCommit)
from community.git import get_org_name


class AffiliatedCommitterModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        org_name = get_org_name()
        most_commits = MostCommit.objects.create(
            project='test project',
            commits='76')
        most_recent_commit = MostRecentCommit.objects.create(
            project='test project',
            date='Jun 2018')
        AffiliatedCommitter.objects.create(
            name='Test User',
            level=2,
            org=org_name,
            most_commits=most_commits,
            most_recent_commit=most_recent_commit)

    def test_field_label(self):
        affiliated_committer = AffiliatedCommitter.objects.get(id=1)

        name = affiliated_committer._meta.get_field('name').verbose_name
        self.assertEquals(name, 'name')

        kudos = affiliated_committer._meta.get_field('kudos').verbose_name
        self.assertEquals(kudos, 'kudos')

        level = affiliated_committer._meta.get_field('level').verbose_name
        self.assertEquals(level, 'level')

        org = affiliated_committer._meta.get_field(
            'org').verbose_name
        self.assertEquals(org, 'org')

        most_commit_project = (
            affiliated_committer.most_commits._meta.get_field(
                'project').verbose_name)
        self.assertEquals(most_commit_project, 'project')

        most_commit_commits = (
            affiliated_committer.most_commits._meta.get_field(
                'commits').verbose_name)
        self.assertEquals(most_commit_commits, 'commits')

        most_recent_commit_project = (
            affiliated_committer.most_recent_commit._meta.get_field(
                'project').verbose_name)
        self.assertEquals(most_recent_commit_project, 'project')

        most_recent_commit_date = (
            affiliated_committer.most_recent_commit._meta.get_field(
                'date').verbose_name)
        self.assertEquals(most_recent_commit_date, 'date')

    def test_char_field_max_length(self):
        affiliated_committer = AffiliatedCommitter.objects.get(id=1)

        name = affiliated_committer._meta.get_field('name').max_length
        self.assertEquals(name, 100)

        org = affiliated_committer._meta.get_field('org').max_length
        self.assertEquals(org, 100)

        most_commit_project = (
            affiliated_committer.most_commits._meta.get_field(
                'project').max_length)
        self.assertEquals(most_commit_project, 100)

        most_recent_commit_project = (
            affiliated_committer.most_recent_commit._meta.get_field(
                'project').max_length)
        self.assertEquals(most_recent_commit_project, 100)

    def test_object_name_is_org_name(self):
        affiliated_committer = AffiliatedCommitter.objects.get(id=1)
        expected_object_name = affiliated_committer.org
        self.assertEquals(expected_object_name, str(affiliated_committer))

    def test_get_absolute_url(self):
        affiliated_committer = AffiliatedCommitter.objects.get(id=1)
        self.assertEquals(affiliated_committer.get_absolute_url(),
                          '/model/openhub/affiliated_committer/1/')
