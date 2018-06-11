from django.test import TestCase
from django.urls import reverse

from data.models import Contributor


class DataViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 10 contributors for the tests
        number_of_contributors = 10
        for i in range(number_of_contributors):
            Contributor.objects.create(login='testuser'+str(i))

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/contributors/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('community-data'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'contributors.html')

    def test_all_contributors_on_template(self):
        resp = self.client.get(reverse('community-data'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['contributors']) == 10)
