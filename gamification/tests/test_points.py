from django.test import TestCase
from gamification.points import get_total_points


class GetTotalPointsTest(TestCase):

    def test_get_total_points(self):
        labels = ['difficulty/newcomer', 'type/bug']

        # Get points when activity is issue
        issue_points = get_total_points('issue', labels)
        self.assertEquals(issue_points, 10)

        # Get points when activity is merge_request
        mr_points = get_total_points('merge_request', labels)
        self.assertEquals(mr_points, 17)

        # Get points when activity type is something else
        with self.assertRaises(ValueError):
            get_total_points('undefined', labels)
