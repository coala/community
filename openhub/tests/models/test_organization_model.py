from django.test import TestCase

from openhub.models import (
    InfographicDetail,
    Organization)


class OrganizationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        infographic_details = InfographicDetail.objects.create(
            outside_committers=3)
        Organization.objects.create(
            name='Test org',
            org_type='Non-Profit',
            infographic_details=infographic_details)

    def test_field_label(self):
        org = Organization.objects.get(id=1)

        name = org._meta.get_field('name').verbose_name
        self.assertEquals(name, 'name')

        url = org._meta.get_field('url').verbose_name
        self.assertEquals(url, 'url')

        html_url = org._meta.get_field('html_url').verbose_name
        self.assertEquals(html_url, 'html url')

        created_at = org._meta.get_field('created_at').verbose_name
        self.assertEquals(created_at, 'created at')

        updated_at = org._meta.get_field('updated_at').verbose_name
        self.assertEquals(updated_at, 'updated at')

        description = org._meta.get_field('description').verbose_name
        self.assertEquals(description, 'description')

        homepage_url = org._meta.get_field('homepage_url').verbose_name
        self.assertEquals(homepage_url, 'homepage url')

        url_name = org._meta.get_field('url_name').verbose_name
        self.assertEquals(url_name, 'url name')

        org_type = org._meta.get_field('org_type').verbose_name
        self.assertEquals(org_type, 'org type')

        medium_logo_url = org._meta.get_field(
            'medium_logo_url').verbose_name
        self.assertEquals(medium_logo_url, 'medium logo url')

        small_logo_url = org._meta.get_field(
            'small_logo_url').verbose_name
        self.assertEquals(small_logo_url, 'small logo url')

        infographic_details = org._meta.get_field(
            'infographic_details').verbose_name
        self.assertEquals(infographic_details, 'infographic details')

        i_details = org.infographic_details

        outside_committers = i_details._meta.get_field(
            'outside_committers').verbose_name
        self.assertEquals(outside_committers, 'outside committers')

        outside_committers_commits = i_details._meta.get_field(
            'outside_committers_commits').verbose_name
        self.assertEquals(outside_committers_commits,
                          'outside committers commits')

        projects_having_outside_commits = i_details._meta.get_field(
            'projects_having_outside_commits').verbose_name
        self.assertEquals(
            projects_having_outside_commits,
            'projects having outside commits')

        portfolio_projects = i_details._meta.get_field(
            'portfolio_projects').verbose_name
        self.assertEquals(portfolio_projects, 'portfolio projects')

        affiliators = i_details._meta.get_field(
            'affiliators').verbose_name
        self.assertEquals(affiliators, 'affiliators')

        affiliators_committing_to_portfolio_projects = (
            i_details._meta.get_field(
                'affiliators_committing_to_portfolio_projects').verbose_name)
        self.assertEquals(
            affiliators_committing_to_portfolio_projects,
            'affiliators committing to portfolio projects')

        affiliator_commits_to_portfolio_projects = i_details._meta.get_field(
            'affiliator_commits_to_portfolio_projects').verbose_name
        self.assertEquals(
            affiliator_commits_to_portfolio_projects,
            'affiliator commits to portfolio projects')

        affiliators_commiting_projects = i_details._meta.get_field(
            'affiliators_commiting_projects').verbose_name
        self.assertEquals(
            affiliators_commiting_projects,
            'affiliators commiting projects')

        outside_projects = i_details._meta.get_field(
            'outside_projects').verbose_name
        self.assertEquals(outside_projects, 'outside projects')

        outside_projects_commits = i_details._meta.get_field(
            'outside_projects_commits').verbose_name
        self.assertEquals(outside_projects_commits, 'outside projects commits')

        affiliators_committing_to_outside_projects = i_details._meta.get_field(
            'affiliators_committing_to_outside_projects').verbose_name
        self.assertEquals(
            affiliators_committing_to_outside_projects,
            'affiliators committing to outside projects')

    def test_char_field_max_length(self):
        org = Organization.objects.get(id=1)

        name = org._meta.get_field('name').max_length
        self.assertEquals(name, 100)

        url_name = org._meta.get_field(
            'url_name').max_length
        self.assertEquals(url_name, 100)

        org_type = org._meta.get_field('org_type').max_length
        self.assertEquals(org_type, 100)

    def test_object_name_is_org_name(self):
        org = Organization.objects.get(id=1)
        expected_object_name = org.name
        self.assertEquals(expected_object_name, str(org))

    def test_get_absolute_url(self):
        org = Organization.objects.get(id=1)
        self.assertEquals(org.get_absolute_url(),
                          '/model/openhub/org/1/')
