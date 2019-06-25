from django.core.management import call_command
from django.test import TestCase

from data.issues import import_issue
from community.git import get_org_name
from data.merge_requests import import_mr
from gamification.models import (
    Level,
    Badge,
    Participant,
    BadgeActivity,
)
from data.contrib_data import import_data
from data.newcomers import active_newcomers

ORG_NAME = get_org_name()


class CreateConfigDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('create_config_data')

    def test_command_create_config_data(self):
        levels = Level.objects.all()

        # There must be 9 levels created
        # as there are 9 levels listed in file config.py
        self.assertEquals(levels.count(), 8)

        b_activities = BadgeActivity.objects.all()
        # There must be 26 badge activities created
        # as there are 26 badge_activities listed in
        # file config.py
        self.assertEquals(b_activities.count(), 26)

        badges = Badge.objects.all()
        # There must be 8 badges created
        # as there are 8 badges listed in
        # file config.py
        self.assertEquals(badges.count(), 10)

        # The Bug Finder badge must have two activities
        badge1 = Badge.objects.get(name='The Bug Finder')
        self.assertEquals(badge1.b_activities.count(), 2)

        # The Bear Hunter badge must have two activities
        badge2 = Badge.objects.get(name='The Bear Hunter')
        self.assertEquals(badge2.b_activities.count(), 2)

        # The Bear Writer badge must have three activities
        badge3 = Badge.objects.get(name='The Bear Writer')
        self.assertEquals(badge3.b_activities.count(), 2)

        # The Bug Solver badge must have two activities
        badge4 = Badge.objects.get(name='The Bug Solver')
        self.assertEquals(badge4.b_activities.count(), 2)

        # The helper badge must have two activities
        badge5 = Badge.objects.get(name='The Helper')
        self.assertEquals(badge5.b_activities.count(), 2)

        # The quick helper badge must have two activities
        badge6 = Badge.objects.get(name='The Quick Helper')
        self.assertEquals(badge6.b_activities.count(), 2)

        # The All-Rounder badge must have two activities
        badge7 = Badge.objects.get(name='The All-Rounder')
        self.assertEquals(badge7.b_activities.count(), 2)


class CreateParticipantsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('create_participants')

    def test_command_create_participants(self):
        participants = Participant.objects.all()
        self.assertEquals(participants.count(), len(active_newcomers()))


class UpdateParticipantsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for contrib in get_false_contributors_data():
            import_data(contrib)

        for issue in get_false_issues_data():
            import_issue('github', issue)

        for mr in get_false_mrs_data():
            import_mr('github', mr)

        for contrib in get_false_active_newcomers():
            Participant.objects.create(username=contrib['username'])

        call_command('import_issues_data')
        call_command('import_merge_requests_data')
        call_command('create_config_data')
        call_command('create_participants')
        call_command('update_participants_data')

    def test_command_update_particiapants_data(self):
        participant = Participant.objects.get(username='testuser')
        number_of_activities = participant.activities.all().count()
        self.assertEquals(number_of_activities, 5)

        score = participant.score
        self.assertEquals(score, 42)

        current_level = participant.level.name
        self.assertEquals(current_level, 'Intermediate-II')

        number_of_badges = participant.badges.all().count()
        self.assertEquals(number_of_badges, 2)


def get_false_contributors_data():
    return [
        {
            'bio': '',
            'teams': [
                f'{ORG_NAME} newcomers'
            ],
            'reviews': 0,
            'issues': 0,
            'name': '',
            'login': 'testuser',
            'contributions': 1
        },
        {
            'bio': '',
            'teams': [
                f'{ORG_NAME} newcomers'
            ],
            'reviews': 0,
            'issues': 0,
            'name': '',
            'login': 'testuser',
            'contributions': 1
        },
        {
            'bio': '',
            'teams': [
            ],
            'reviews': 0,
            'name': '',
            'login': 'testuser1',
            'contributions': 1
        }
    ]


def get_false_issues_data():
    return [
        {
            'created_at': '2016-11-21T00:46:14',
            'hoster': 'github',
            'updated_at': '2017-12-21T00:00:48',
            'labels': [
                'status/duplicate'
            ],
            'number': 1,
            'assignees': [],
            'repo_id': 254525111,
            'title': 'Test issue',
            'state': 'closed',
            'repo': f'{ORG_NAME}/{ORG_NAME}',
            'url': f'https://github.com/{ORG_NAME}/corobo/issues/585',
            'author': 'testuser'
        },
        {
            'created_at': '2016-11-21T00:46:14',
            'hoster': 'github',
            'updated_at': '2017-12-21T00:00:48',
            'labels': [
                'difficulty/newcomer',
                'type/bug'
            ],
            'number': 3,
            'assignees': [],
            'repo_id': 254525111,
            'title': 'Test issue',
            'state': 'closed',
            'repo': f'{ORG_NAME}/{ORG_NAME}',
            'url': f'https://github.com/{ORG_NAME}/{ORG_NAME}/issues/1',
            'author': 'testuser1'
        },
        {
            'created_at': '2016-11-21T00:46:14',
            'hoster': 'github',
            'updated_at': '2017-12-21T00:00:48',
            'labels': [
                'difficulty/newcomer',
                'type/bug'
            ],
            'number': 2,
            'assignees': [],
            'repo_id': 254525111,
            'title': 'Test issue',
            'state': 'closed',
            'repo': f'{ORG_NAME}/{ORG_NAME}',
            'url': f'https://github.com/{ORG_NAME}/{ORG_NAME}/issues/2',
            'author': 'testuser'
        },
        {
            'created_at': '2016-11-21T00:46:14',
            'hoster': 'github',
            'updated_at': '2017-12-21T00:00:48',
            'labels': [
                'difficulty/newcomer',
                'type/bug'
            ],
            'number': 2,
            'assignees': [],
            'title': 'Test issue',
            'state': 'closed',
            'repo': 'test/test',
            'url': f'https://github.com/{ORG_NAME}/{ORG_NAME}/issues/3',
            'author': 'testuser1'
        }
    ]


def get_false_mrs_data():
    return [
        {
            'created_at': '2016-02-21T05:04:25',
            'hoster': 'github',
            'ci_status': True,
            'labels': [
                'difficulty/newcomer',
                'type/bug'
            ],
            'title': 'Test merge request-I',
            'number': 1625,
            'updated_at': '2016-04-21T12:06:19',
            'assignees': [],
            'repo_id': 254525111,
            'closes_issues': [
                2,
                3
            ],
            'repo': f'{ORG_NAME}/{ORG_NAME}',
            'url': f'https://github.com/{ORG_NAME}/{ORG_NAME}/pull/1625',
            'state': 'merged',
            'author': 'testuser'
        },
        {
            'created_at': '2016-02-21T05:04:25',
            'hoster': 'github',
            'ci_status': True,
            'labels': [
                'status/STALE'
            ],
            'title': 'Test merge request-II',
            'number': 1626,
            'updated_at': '2016-02-21T12:06:19',
            'assignees': [],
            'repo_id': 25452511,
            'closes_issues': [
            ],
            'repo': f'{ORG_NAME}/{ORG_NAME}',
            'state': 'merged',
            'url': f'https://github.com/{ORG_NAME}/{ORG_NAME}/pull/1626',
            'author': 'testuser'
        },
        {
            'created_at': '2016-02-21T05:04:25',
            'hoster': 'github',
            'ci_status': True,
            'labels': [
                'difficulty/low',
                'type/bug'
            ],
            'title': 'Test merge request-III',
            'number': 1626,
            'updated_at': '2016-02-21T12:06:19',
            'assignees': [
                'testuser',
                'testuser1'
            ],
            'repo_id': 25452511,
            'closes_issues': [
            ],
            'repo': f'{ORG_NAME}/{ORG_NAME}',
            'state': 'merged',
            'url': f'https://github.com/{ORG_NAME}/{ORG_NAME}/pull/1625',
            'author': 'testuser'
        },
        {
            'created_at': '2016-02-21T05:04:25',
            'hoster': 'github',
            'labels': [
                'difficulty/low',
                'type/bug'
            ],
            'title': 'Test merge request-III',
            'number': 1626,
            'updated_at': '2016-02-21T12:06:19',
            'assignees': [],
            'repo_id': 25452511,
            'repo': f'{ORG_NAME}/{ORG_NAME}',
            'url': f'https://github.com/{ORG_NAME}/{ORG_NAME}/pull/1625',
            'closes_issues': [
            ],
            'author': 'testuser1'
        }
    ]


def get_false_active_newcomers():
    return [
        {'username': 'testuser'},
        {'username': 'testuser1'}
    ]
