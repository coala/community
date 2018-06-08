from django.core.management.base import BaseCommand

from meta_review.handler import handle as handle_meta_review


class Command(BaseCommand):
    help = 'Scrape, process and store data'

    def handle(self, *args, **options):
        handle_meta_review()
