from django.test import TestCase
from django.urls import reverse

from gamification.models import Participant


class GamificationViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 10 participants for the tests
        number_of_participants = 10
        for i in range(number_of_participants):
            Participant.objects.create(username='usertest'+str(i))

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/gamification/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('community-gamification'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'gamification.html')

    def test_all_contributors_on_template(self):
        resp = self.client.get(reverse('community-gamification'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['participants']) == 10)
