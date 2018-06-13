from django.test import TestCase

from openhub.models import OpenhubOrganization
from community.git import get_org_name


class OpenhubOrganizationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        org_name = get_org_name()
        OpenhubOrganization.objects.create(name='test', org_type='Commercial')
        OpenhubOrganization.objects.create(name=org_name, org_type='Non-Profit')

    def test_field_label(self):
        openhub_org = OpenhubOrganization.objects.get(id=1)

        name = openhub_org._meta.get_field('name').verbose_name
        self.assertEquals(name, 'name')

        url = openhub_org._meta.get_field('url').verbose_name
        self.assertEquals(url, 'url')

        html_url = openhub_org._meta.get_field('html_url').verbose_name
        self.assertEquals(html_url, 'html url')

        created_at = openhub_org._meta.get_field('created_at').verbose_name
        self.assertEquals(created_at, 'created at')

        updated_at = openhub_org._meta.get_field('updated_at').verbose_name
        self.assertEquals(updated_at, 'updated at')

        description = openhub_org._meta.get_field('description').verbose_name
        self.assertEquals(description, 'description')

        homepage_url = openhub_org._meta.get_field('homepage_url').verbose_name
        self.assertEquals(homepage_url, 'homepage url')

        vanity_url = openhub_org._meta.get_field('vanity_url').verbose_name
        self.assertEquals(vanity_url, 'vanity url')

        org_type = openhub_org._meta.get_field('org_type').verbose_name
        self.assertEquals(org_type, 'org type')

        medium_logo_url = openhub_org._meta.get_field(
            'medium_logo_url').verbose_name
        self.assertEquals(medium_logo_url, 'medium logo url')

        small_logo_url = openhub_org._meta.get_field(
            'small_logo_url').verbose_name
        self.assertEquals(small_logo_url, 'small logo url')

        projects_count = openhub_org._meta.get_field(
            'projects_count').verbose_name
        self.assertEquals(projects_count, 'projects count')

        affiliated_committers = openhub_org._meta.get_field(
            'affiliated_committers').verbose_name
        self.assertEquals(affiliated_committers, 'affiliated committers')

    def test_char_field_max_length(self):
        openhub_org = OpenhubOrganization.objects.get(id=1)

        name_max_length = openhub_org._meta.get_field('name').max_length
        self.assertEquals(name_max_length, 100)

        vanity_url_max_length = openhub_org._meta.get_field(
            'vanity_url').max_length
        self.assertEquals(vanity_url_max_length, 200)

        org_type_max_length = openhub_org._meta.get_field('org_type').max_length
        self.assertEquals(org_type_max_length, 100)

    def test_object_name_is_org_name(self):
        openhub_org = OpenhubOrganization.objects.get(id=1)
        expected_object_name = openhub_org.name
        self.assertEquals(expected_object_name, str(openhub_org))

    def test_class_meta_ordering(self):
        org_name = get_org_name()
        openhub_orgs = OpenhubOrganization.objects.all()
        self.assertEquals(openhub_orgs[0].name, org_name)
        self.assertEquals(openhub_orgs[1].name, 'test')
