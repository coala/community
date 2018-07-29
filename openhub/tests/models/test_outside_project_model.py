from django.test import TestCase

from openhub.models import OutsideProject


class OutsideProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        OutsideProject.objects.create(
            name='Test project',
            activity='High', org='Test')

    def test_field_label(self):
        outside_project = OutsideProject.objects.get(id=1)

        name = outside_project._meta.get_field('name').verbose_name
        self.assertEquals(name, 'name')

        activity = outside_project._meta.get_field('activity').verbose_name
        self.assertEquals(activity, 'activity')

        claimed_by = outside_project._meta.get_field('claimed_by').verbose_name
        self.assertEquals(claimed_by, 'claimed by')

        i_use_this = outside_project._meta.get_field(
            'i_use_this').verbose_name
        self.assertEquals(i_use_this, 'i use this')

        affiliates_contributing = outside_project._meta.get_field(
            'affiliates_contributing').verbose_name
        self.assertEquals(affiliates_contributing, 'affiliates contributing')

        commits_by_current_affiliates = outside_project._meta.get_field(
            'commits_by_current_affiliates').verbose_name
        self.assertEquals(commits_by_current_affiliates,
                          'commits by current affiliates')

        org = outside_project._meta.get_field('org').verbose_name
        self.assertEquals(org, 'org')

    def test_char_field_max_length(self):
        outside_project = OutsideProject.objects.get(id=1)

        name_max_length = outside_project._meta.get_field('name').max_length
        self.assertEquals(name_max_length, 100)

        activity_max_length = outside_project._meta.get_field(
            'activity').max_length
        self.assertEquals(activity_max_length, 100)

        claimed_by_max_length = outside_project._meta.get_field(
            'claimed_by').max_length
        self.assertEquals(claimed_by_max_length, 100)

        org = outside_project._meta.get_field('org').max_length
        self.assertEquals(org, 100)

    def test_object_name_is_project_name(self):
        outside_project = OutsideProject.objects.get(id=1)
        expected_object_name = outside_project.name
        self.assertEquals(expected_object_name, str(outside_project))

    def test_get_absolute_url(self):
        outside_project = OutsideProject.objects.get(id=1)
        self.assertEquals(outside_project.get_absolute_url(),
                          '/model/openhub/outside_project/1/')
