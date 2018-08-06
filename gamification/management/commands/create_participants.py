from django.core.management.base import BaseCommand

from gamification.participants import create_participants


class Command(BaseCommand):
    help = 'Create Participants'

    def handle(self, *args, **options):
        create_participants()
