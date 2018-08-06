import logging

from django.db import models


class Activity(models.Model):
    name = models.TextField()
    points = models.IntegerField()

    # Which time this activity is being performed by the same
    # participant.
    # Note that this field is not in use atm.
    number_of_times = models.IntegerField(default=1, null=True)

    # Participant who performs this activity
    performer = models.ForeignKey('Participant',
                                  on_delete=models.CASCADE,
                                  null=True)
    # The date and time this activity was performed
    performed_at = models.DateTimeField(null=True)

    # The date and time this activity was last updated
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Level(models.Model):
    number = models.IntegerField(primary_key=True)
    min_score = models.BigIntegerField()
    max_score = models.BigIntegerField()
    name = models.TextField()

    def __str__(self):
        return self.name


class BadgeActivity(models.Model):
    name = models.TextField()

    # Number of times a participant have to perform this activity
    # to get this badge. Note that this field is not in use atm.
    number_of_times = models.IntegerField(default=1, null=True)

    def __str__(self):
        return self.name


class Badge(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    details = models.TextField(null=True)

    # Activities a participant have to perform to get this badge
    b_activities = models.ManyToManyField(BadgeActivity)

    def __str__(self):
        return self.name


class Participant(models.Model):
    username = models.CharField(max_length=100, primary_key=True)

    # Total points earned by the participant
    score = models.IntegerField(default=0, null=True)

    # Current level
    level = models.ForeignKey(Level, on_delete=models.CASCADE,
                              default=1, null=True)

    # All the activities performed
    activities = models.ManyToManyField(Activity)

    # Badges earned by participant
    badges = models.ManyToManyField(Badge)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-score']

    def add_points(self, points, activity_string, performed_at, updated_at):
        """
        Update score, level and add activities peformed.

        :param points:          an integer value representing the
                                points earned by the participant
                                for performing an activity.
        :param activity_string: a string representing the activity
                                performed by the participant.
        :param performed_at:    a datetime object representing the date
                                and time when this activity was performed.
        :param updated_at:      a datetime object representing the date and time when
                                this activity was performed.
        """
        self.update_score_and_level(points)
        self.add_activity(points,
                          activity_string,
                          performed_at,
                          updated_at,
                          )

    def deduct_points(self, points_to_deduct, activity_string,
                      performed_at, updated_at):
        """
        Deduct points for performing some specific activities.
        """
        self.add_points(points_to_deduct,
                        activity_string,
                        performed_at,
                        updated_at,
                        )

    def find_level_for_score(self, score):
        """
        Find suitable level based on the total score earned.
        """
        level = Level.objects.get(min_score__lte=score, max_score__gt=score)
        return level

    def update_score_and_level(self, points):
        """
        Update score and level based on points.
        """
        if points < 0 and self.score < abs(points):
            self.score = 0
        else:
            self.score += points

        self.level = self.find_level_for_score(self.score)
        self.save()

    def add_activity(self, points, activity_string, performed_at, updated_at):
        """
        Add a new activity to the participant.
        """
        activity = Activity.objects.create(
            name=activity_string,
            points=points,
            performer=self,
            performed_at=performed_at,
            updated_at=updated_at)
        self.activities.add(activity)

    def find_badges_for_activity(self, activities):
        """
        Find the badge based on the activities peformed by the participant.

        :param activities: a QuerySet dict containing the 'name'
                           as key and 'name of the activity' as value.
        :return:           a badge object.
        """
        logger = logging.getLogger(__name__)
        activities = [activity['name'] for activity in activities]
        badge_objects_list = []
        badges = Badge.objects.all()
        for badge in badges:
            b_activities = badge.b_activities.values('name')
            b_activities = [b_activity['name'] for b_activity in b_activities]
            # Skip the badge which have no activities
            if not len(b_activities):
                logger.info('Badge: %s have no activities.' % badge)
                continue
            match_activity_list = []
            for b_activity in b_activities:
                b_activity_words_list = b_activity.split()
                for activity in activities:
                    if all(x in activity for x in b_activity_words_list):
                        match_activity_list.append(1)
                        break
            if len(b_activities) == len(match_activity_list):
                # The participant have performed all the activities listed
                # in the badge
                badge_objects_list.append(badge)
                logger.debug(
                    'Participant: %s is awarded with %s badge.' % (self, badge))

        return badge_objects_list

    def add_badges(self, activities):
        """
        Add badges to participant based on the activities performed.
        """
        badges = self.find_badges_for_activity(activities)
        for badge in badges:
            self.badges.add(badge)
