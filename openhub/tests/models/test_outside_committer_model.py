from django.test import TestCase

from openhub.models import (
    OutsideCommitter,
    ContributionsToPortfolioProject)
from community.git import get_org_name


class OutsideCommitterModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        org_name = get_org_name()
        cpp = ContributionsToPortfolioProject.objects.create(
            projects='test_project-1, test_project-2',
            twelve_mo_commits=49
            )
        OutsideCommitter.objects.create(
            name='Test User',
            level=2,
            affiliated_with='Unaffiliated',
            org=org_name,
            contributions_to_portfolio_projects=cpp
            )

    def test_field_label(self):
        outside_committer = OutsideCommitter.objects.get(id=1)

        name = outside_committer._meta.get_field('name').verbose_name
        self.assertEquals(name, 'name')

        kudos = outside_committer._meta.get_field('kudos').verbose_name
        self.assertEquals(kudos, 'kudos')

        level = outside_committer._meta.get_field('level').verbose_name
        self.assertEquals(level, 'level')

        affiliated_with = outside_committer._meta.get_field(
            'affiliated_with').verbose_name
        self.assertEquals(affiliated_with, 'affiliated with')

        contributions_to_portfolio_projects = outside_committer._meta.get_field(
            'contributions_to_portfolio_projects').verbose_name
        self.assertEquals(
            contributions_to_portfolio_projects,
            'contributions to portfolio projects')

        cpp = outside_committer.contributions_to_portfolio_projects
        projects = cpp._meta.get_field(
            'projects').verbose_name
        self.assertEquals(projects, 'projects')

        twelve_mo_commits = cpp._meta.get_field(
            'twelve_mo_commits').verbose_name
        self.assertEquals(twelve_mo_commits, 'twelve mo commits')

    def test_char_field_max_length(self):
        outside_committer = OutsideCommitter.objects.get(id=1)

        name_max_length = outside_committer._meta.get_field('name').max_length
        self.assertEquals(name_max_length, 100)

        affiliated_with_max_length = outside_committer._meta.get_field(
            'affiliated_with').max_length
        self.assertEquals(affiliated_with_max_length, 100)

        org = outside_committer._meta.get_field('org').max_length
        self.assertEquals(org, 100)

    def test_object_name_is_committer_name(self):
        outside_committer = OutsideCommitter.objects.get(id=1)
        expected_object_name = outside_committer.name
        self.assertEquals(expected_object_name, str(outside_committer))

    def test_get_absolute_url(self):
        outside_committer = OutsideCommitter.objects.get(id=1)
        self.assertEquals(outside_committer.get_absolute_url(),
                          '/model/openhub/outside_committer/1/')
