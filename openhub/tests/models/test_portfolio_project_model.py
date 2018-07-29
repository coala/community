from django.test import TestCase

from openhub.models import (
    PortfolioProjectActivity,
    PortfolioProject,
    )
from community.git import get_org_name


class PortfolioProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        project_activity = PortfolioProjectActivity.objects.create(commits=3)
        org_name = get_org_name()
        PortfolioProject.objects.create(
            name='community',
            activity='Moderate',
            i_use_this='45',
            org=org_name,
            primary_language='python',
            twelve_mo_activity_and_year_on_year_change=project_activity)

    def test_field_label(self):
        portfolio_project = PortfolioProject.objects.get(id=1)

        name = portfolio_project._meta.get_field('name').verbose_name
        self.assertEquals(name, 'name')

        activity = portfolio_project._meta.get_field('activity').verbose_name
        self.assertEquals(activity, 'activity')

        i_use_this = portfolio_project._meta.get_field(
            'i_use_this').verbose_name
        self.assertEquals(i_use_this, 'i use this')

        community_rating = portfolio_project._meta.get_field(
            'community_rating').verbose_name
        self.assertEquals(community_rating, 'community rating')

        primary_language = portfolio_project._meta.get_field(
            'primary_language').verbose_name
        self.assertEquals(primary_language, 'primary language')

        twelve_mo_activity_and_year_on_year_change = (
            portfolio_project._meta.get_field(
                'twelve_mo_activity_and_year_on_year_change').verbose_name)
        self.assertEquals(
            twelve_mo_activity_and_year_on_year_change,
            'twelve mo activity and year on year change')

        activity_change = (
            portfolio_project.twelve_mo_activity_and_year_on_year_change)
        commits = activity_change._meta.get_field('commits').verbose_name
        self.assertEquals(commits, 'commits')

        change_in_commits = activity_change._meta.get_field(
            'change_in_commits').verbose_name
        self.assertEquals(change_in_commits, 'change in commits')

        percentage_change_in_commits = activity_change._meta.get_field(
            'percentage_change_in_commits').verbose_name
        self.assertEquals(percentage_change_in_commits,
                          'percentage change in commits')

        contributors = activity_change._meta.get_field(
            'contributors').verbose_name
        self.assertEquals(contributors, 'contributors')

        change_in_contributors = activity_change._meta.get_field(
            'change_in_contributors').verbose_name
        self.assertEquals(change_in_contributors, 'change in contributors')

        percentage_change_in_committers = activity_change._meta.get_field(
            'percentage_change_in_committers').verbose_name
        self.assertEquals(percentage_change_in_committers,
                          'percentage change in committers')

    def test_char_field_max_length(self):
        portfolio_project = PortfolioProject.objects.get(id=1)

        name_max_length = portfolio_project._meta.get_field('name').max_length
        self.assertEquals(name_max_length, 100)

        activity = portfolio_project._meta.get_field('activity').max_length
        self.assertEquals(activity, 100)

        primary_language = portfolio_project._meta.get_field(
            'primary_language').max_length
        self.assertEquals(primary_language, 100)

        org = portfolio_project._meta.get_field('org').max_length
        self.assertEquals(org, 200)

    def test_object_name_is_project_name(self):
        portfolio_project = PortfolioProject.objects.get(id=1)
        expected_object_name = portfolio_project.name
        self.assertEquals(expected_object_name, str(portfolio_project))
