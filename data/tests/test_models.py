from django.test import TestCase

from data.models import Contributor


class ContributorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        Contributor.objects.create(login='test', name='Test User')
        Contributor.objects.create(login='sks444', name='Shrikrishna Singh')

    def test_field_label(self):
        contributor = Contributor.objects.get(login='sks444')
        login = contributor._meta.get_field('login').verbose_name
        name = contributor._meta.get_field('name').verbose_name
        bio = contributor._meta.get_field('bio').verbose_name
        num_commits = (
            contributor._meta.get_field('num_commits').verbose_name)
        reviews = contributor._meta.get_field('reviews').verbose_name
        issues_opened = contributor._meta.get_field(
            'issues_opened').verbose_name
        self.assertEquals(login, 'login')
        self.assertEquals(name, 'name')
        self.assertEquals(bio, 'bio')
        self.assertEquals(num_commits, 'num commits')
        self.assertEquals(reviews, 'reviews')
        self.assertEquals(issues_opened, 'issues opened')

    def test_object_name_is_login(self):
        contributor = Contributor.objects.get(login='sks444')
        expected_object_name = 'sks444'
        self.assertEquals(expected_object_name, str(contributor))

    def test_class_meta_ordering(self):
        contributors = Contributor.objects.all()
        self.assertEquals(contributors[0].login, 'sks444')
        self.assertEquals(contributors[1].login, 'test')
