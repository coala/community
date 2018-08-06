from django.test import TestCase
from gamification.process.activity import get_activity


class GetActivityTest(TestCase):

    def test_issue_activity(self):
        labels = ['difficulty/newcomer', 'type/bug']
        activity = get_activity('issue', labels)

        # There are two labels 'difficulty/newcomer' and 'type/bug'
        # and the activity_type is issue, so the activity should be
        expected_activity = 'Created a difficulty/newcomer type/bug issue'
        self.assertEquals(activity, expected_activity)

    def test_mr_activity(self):
        labels = ['difficulty/newcomer', 'type/bug']
        activity = get_activity('merge_request', labels)

        # There are two labels 'difficulty/newcomer' and 'type/bug'
        # and the activity_type is mr, so the activity should be
        expected_activity = 'Solved a difficulty/newcomer type/bug issue'
        self.assertEquals(activity, expected_activity)

    def test_undefined_activity(self):
        labels = ['difficulty/newcomer', 'type/bug']
        with self.assertRaises(ValueError):
            get_activity('undefined', labels)
