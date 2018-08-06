from django.test import TestCase
from gamification.process.activity_points import get_activity_with_points
from data.models import Label


class GetActivityTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Label.objects.create(name='difficulty/newcomer')
        Label.objects.create(name='type/bug')

    def test_issue_activity_with_points(self):
        labels = Label.objects.values('name')
        points, activity = get_activity_with_points('issue', labels)

        # There are two labels 'difficulty/newcomer' and 'type/bug'
        # and the activity_type is issue, so the activity should be:
        expected_activity = 'Created a difficulty/newcomer type/bug issue'

        # And the points should be:
        expected_points = 10

        self.assertEquals(expected_activity, activity)
        self.assertEquals(expected_points, points)

    def test_mr_activity(self):
        labels = Label.objects.values('name')
        points, activity = get_activity_with_points('merge_request', labels)

        # There are two labels 'difficulty/newcomer' and 'type/bug'
        # and the activity_type is mr, so the activity should be
        expected_activity = 'Solved a difficulty/newcomer type/bug issue'

        # And the points should be:
        expected_points = 17

        self.assertEquals(expected_activity, activity)
        self.assertEquals(expected_points, points)

    def test_undefined_actvitiy(self):
        labels = Label.objects.values('name')
        with self.assertRaises(ValueError):
            get_activity_with_points('undefined', labels)
