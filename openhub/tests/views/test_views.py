from django.test import TestCase
from django.urls import reverse

from openhub.models import (
    PortfolioProject,
    PortfolioProjectActivity)
from community.git import get_org_name


class OpenhubViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 10 portfolio projects for the tests
        org_name = get_org_name()
        project_activity = PortfolioProjectActivity.objects.create(commits=3)
        number_of_projects = 10
        for i in range(number_of_projects):
            PortfolioProject.objects.create(
                name='community'+str(i),
                activity='Moderate',
                i_use_this='45',
                org=org_name,
                primary_language='python',
                twelve_mo_activity_and_year_on_year_change=project_activity)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/openhub/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('community-openhub'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'openhub.html')

    def test_all_contributors_on_template(self):
        resp = self.client.get(reverse('community-openhub'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['projects']) == 10)
