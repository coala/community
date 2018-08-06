from django.core.management.base import BaseCommand

from gamification.data.config import (
    create_levels,
    create_badge_activities,
    create_badges,
    add_activities_to_badges,
)


class Command(BaseCommand):
    help = 'Create config data'

    def handle(self, *args, **options):
        create_levels()
        create_badge_activities()
        create_badges()
        add_activities_to_badges()
