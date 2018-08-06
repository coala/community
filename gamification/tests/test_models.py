from django.test import TestCase

from gamification.models import (
    Activity,
    Level,
    BadgeActivity,
    Badge,
    Participant,
)


class ActivityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        Activity.objects.create(
            name='Created a difficulty/newcomer type/bug issue',
            points=10)

    def test_field_label(self):
        activity = Activity.objects.get(id=1)
        name = activity._meta.get_field('name').verbose_name
        points = activity._meta.get_field('points').verbose_name
        number_of_times = activity._meta.get_field(
            'number_of_times').verbose_name
        performer = activity._meta.get_field(
            'performer').verbose_name
        performed_at = activity._meta.get_field(
            'performed_at').verbose_name
        updated_at = activity._meta.get_field(
            'updated_at').verbose_name
        self.assertEquals(name, 'name')
        self.assertEquals(points, 'points')
        self.assertEquals(number_of_times, 'number of times')
        self.assertEquals(performer, 'performer')
        self.assertEquals(updated_at, 'updated at')
        self.assertEquals(performed_at, 'performed at')

    def test_object_name_is_activity_name(self):
        activity = Activity.objects.get(id=1)
        expected_object_name = (
            'Created a difficulty/newcomer type/bug issue')
        self.assertEquals(expected_object_name, str(activity))


class LevelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        Level.objects.create(number=1,
                             min_score=0, max_score=5, name='Fresher')

    def test_field_label(self):
        level = Level.objects.get(number=1)
        number = level._meta.get_field('number').verbose_name
        min_score = level._meta.get_field('min_score').verbose_name
        max_score = level._meta.get_field('max_score').verbose_name
        name = level._meta.get_field('name').verbose_name
        self.assertEquals(number, 'number')
        self.assertEquals(min_score, 'min score')
        self.assertEquals(max_score, 'max score')
        self.assertEquals(name, 'name')

    def test_object_name_is_lavel_name(self):
        level = Level.objects.get(number=1)
        expected_object_name = 'Fresher'
        self.assertEquals(expected_object_name, str(level))


class BadgeActivityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        BadgeActivity.objects.create(
            name='Created a difficulty/newcomer type/bug issue')

    def test_field_label(self):
        b_activity = BadgeActivity.objects.get(id=1)
        name = b_activity._meta.get_field('name').verbose_name
        number_of_times = b_activity._meta.get_field(
            'number_of_times').verbose_name
        self.assertEquals(name, 'name')
        self.assertEquals(number_of_times, 'number of times')

    def test_object_name_is_badge_activity_name(self):
        b_activity = BadgeActivity.objects.get(id=1)
        expected_object_name = (
            'Created a difficulty/newcomer type/bug issue')
        self.assertEquals(expected_object_name, str(b_activity))


class BadgeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        BadgeActivity.objects.create(
            name='Created a difficulty/newcomer type/bug issue')
        Badge.objects.create(
            number=1,
            name='The Bug Finder')

    def test_field_label(self):
        badge = Badge.objects.get(number=1)
        number = badge._meta.get_field('number').verbose_name
        name = badge._meta.get_field('name').verbose_name
        details = badge._meta.get_field('details').verbose_name
        b_activities = badge._meta.get_field(
            'b_activities').verbose_name
        self.assertEquals(number, 'number')
        self.assertEquals(name, 'name')
        self.assertEquals(details, 'details')
        self.assertEquals(b_activities, 'b activities')

    def test_object_name_is_badge_name(self):
        badge = Badge.objects.get(number=1)
        expected_object_name = 'The Bug Finder'
        self.assertEquals(expected_object_name, str(badge))

    def test_many_to_many_field(self):
        badge = Badge.objects.get(number=1)
        b_activity = BadgeActivity.objects.get(id=1)
        badge.b_activities.add(b_activity)
        self.assertEquals(badge.b_activities.get(pk=b_activity.pk),
                          b_activity)


class ParticipantModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        Level.objects.create(number=1,
                             min_score=0, max_score=5,
                             name='Fresher')
        Level.objects.create(number=2,
                             min_score=5, max_score=20,
                             name='Beginner-I')
        b_activity1 = BadgeActivity.objects.create(
            name='Created a difficulty/newcomer type/bug issue')
        b_activity2 = BadgeActivity.objects.create(
            name='Created a difficulty/low type/bug issue')
        b_activity3 = BadgeActivity.objects.create(
            name='Created a area/documentation issue')
        b_activity4 = BadgeActivity.objects.create(
            name='Solved a area/documentation issue')
        badge1 = Badge.objects.create(
            number=1,
            name='The Bug Finder')
        badge1.b_activities.add(*[b_activity1, b_activity2])
        badge2 = Badge.objects.create(
            number=2,
            name='The Doc-Care')
        badge2.b_activities.add(*[b_activity3, b_activity4])
        Badge.objects.create(
            number=3,
            name='The Helper')
        Activity.objects.create(
            name='Created a difficulty/newcomer type/bug issue',
            points=10)
        Activity.objects.create(
            name='Created a difficulty/low type/bug issue',
            points=12)
        Activity.objects.create(
            name='Solved a difficulty/newcomer type/bug issue',
            points=12)
        Activity.objects.create(
            name='Solved a area/documentation issue',
            points=7)
        Participant.objects.create(username='sks444')
        Participant.objects.create(username='test')

    def test_field_label(self):
        participant = Participant.objects.get(username='sks444')
        username = participant._meta.get_field(
            'username').verbose_name
        score = participant._meta.get_field('score').verbose_name
        level = participant._meta.get_field('level').verbose_name
        activities = participant._meta.get_field(
            'activities').verbose_name
        badges = participant._meta.get_field(
            'badges').verbose_name
        self.assertEquals(username, 'username')
        self.assertEquals(score, 'score')
        self.assertEquals(level, 'level')
        self.assertEquals(activities, 'activities')
        self.assertEquals(badges, 'badges')

    def test_object_name_is_participant_username(self):
        participant = Participant.objects.get(username='sks444')
        expected_object_name = 'sks444'
        self.assertEquals(expected_object_name,
                          str(participant))

    def test_class_meta_ordering(self):
        participant1 = Participant.objects.get(username='sks444')
        participant1.score = 5
        participant1.save()
        participant2 = Participant.objects.get(username='test')
        participant2.score = 10
        participant2.save()
        participants = Participant.objects.all()
        self.assertEquals(participants[0].username, 'test')
        self.assertEquals(participants[1].username, 'sks444')

    def test_add_points_method(self):
        participant = Participant.objects.get(username='sks444')
        points = 10
        activity_string = 'Created a difficulty/newcomer bug issue'
        performed_at = '2017-08-24 05:59:31+00:00'
        updated_at = '2018-06-02 17:06:18+00:00'
        participant.add_points(points,
                               activity_string,
                               performed_at,
                               updated_at,
                               )
        self.assertEquals(participant.score, 10)
        self.assertEquals(participant.level.name, 'Beginner-I')
        self.assertEquals(participant.activities.count(), 1)

    def test_deduct_points_method(self):
        participant = Participant.objects.get(username='sks444')
        participant.score = 5
        participant.save()
        points = -5
        activity_string = 'Merge request was closed without merge'
        performed_at = '2017-08-24 05:59:31+00:00'
        updated_at = '2018-06-02 17:06:18+00:00'
        participant.deduct_points(points,
                                  activity_string,
                                  performed_at,
                                  updated_at,
                                  )
        self.assertEquals(participant.score, 0)
        self.assertEquals(participant.level.name, 'Fresher')
        self.assertEquals(participant.activities.count(), 1)

    def test_find_level_for_score_method(self):
        participant = Participant.objects.get(username='sks444')
        level = participant.find_level_for_score(10)
        self.assertEquals(level.name, 'Beginner-I')

    def test_update_score_and_level_method(self):
        participant = Participant.objects.get(username='sks444')
        # Before update
        self.assertEquals(participant.score, 0)
        self.assertEquals(participant.level.name, 'Fresher')

        # Update
        participant.update_score_and_level(7)

        # After update
        self.assertEquals(participant.score, 7)
        self.assertEquals(participant.level.name, 'Beginner-I')

        # Update with less negative points
        participant.update_score_and_level(-2)
        self.assertEquals(participant.score, 5)
        self.assertEquals(participant.level.name, 'Beginner-I')

        # Test with more negative points
        participant.update_score_and_level(-10)
        self.assertEquals(participant.score, 0)
        self.assertEquals(participant.level.name, 'Fresher')

    def test_add_activity_method(self):
        participant = Participant.objects.get(username='sks444')

        # Befor applying add_activity
        self.assertEquals(participant.activities.count(), 0)

        # Apply add_activity
        points = 5
        activity = 'Created a difficulty/newcomer type/bug issue'
        performed_at = '2017-08-24 05:59:31+00:00'
        updated_at = '2018-06-02 17:06:18+00:00'
        participant.add_activity(points,
                                 activity,
                                 performed_at,
                                 updated_at,
                                 )

        # After applying add_activity
        self.assertEquals(participant.activities.count(), 1)

        # Performing the same activity again which means that a
        # new activity should be added.
        performed_at = '2017-08-23 05:59:31+00:00'
        updated_at = '2018-06-01 17:06:18+00:00'
        participant.add_activity(points,
                                 activity,
                                 performed_at,
                                 updated_at,
                                 )

        # A new activity is added
        self.assertEquals(participant.activities.count(), 2)

    def test_find_badges_for_activity_method(self):
        participant = Participant.objects.get(username='sks444')
        activity1 = Activity.objects.get(id=1)
        activity2 = Activity.objects.get(id=2)
        activity3 = Activity.objects.get(id=3)
        activity4 = Activity.objects.get(id=4)
        participant.activities.add(
            *[activity1, activity2, activity3, activity4])
        activities = participant.activities.values('name')
        badges = participant.find_badges_for_activity(activities)
        self.assertEquals(len(badges), 1)
        self.assertEquals(badges[0].name, 'The Bug Finder')

    def test_add_badges_method(self):
        participant = Participant.objects.get(username='sks444')
        activity1 = Activity.objects.get(id=1)
        activity2 = Activity.objects.get(id=2)
        activity3 = Activity.objects.get(id=3)
        participant.activities.add(*[activity1, activity2, activity3])

        # Before applying add_badge method
        self.assertEquals(participant.badges.count(), 0)

        # Applying add_badge method
        activities = participant.activities.values('name')
        participant.add_badges(activities)

        # After applying add_badge method
        self.assertEquals(participant.badges.count(), 1)

        # Test the participant who has zero activity
        test_participant = Participant.objects.get(username='test')

        # Before applying add_badge method
        self.assertEquals(test_participant.badges.count(), 0)

        # Applying add_badge method
        test_activities = participant.activities.values('name')
        participant.add_badges(test_activities)

        # After applying add_badge method
        self.assertEquals(test_participant.badges.count(), 0)
