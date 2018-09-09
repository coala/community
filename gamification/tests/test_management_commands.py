from django.core.management import call_command
from django.test import TestCase

from gamification.models import (
    Level,
    Badge,
    Participant,
    BadgeActivity,
)
from data.newcomers import active_newcomers


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
        # There must be 27 badge activities created
        # as there are 27 badge_activities listed in
        # file config.py
        self.assertEquals(b_activities.count(), 27)

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
        self.assertEquals(badge7.b_activities.count(), 3)


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
        self.assertEquals(number_of_badges, 1)
