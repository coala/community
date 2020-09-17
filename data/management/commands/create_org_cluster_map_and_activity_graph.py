from django.core.management.base import BaseCommand

from data.org_cluster_map_handler import handle as org_cluster_map_handler
from activity.scraper import activity_json


class Command(BaseCommand):
    help = 'Create a cluster map using contributors geolocation'

    def add_arguments(self, parser):
        parser.add_argument('output_dir', nargs='?', type=str)

    def handle(self, *args, **options):
        output_dir = options.get('output_dir')
        if not output_dir:
            org_cluster_map_handler()
        else:
            org_cluster_map_handler(output_dir)
        # Fetch & Store data for activity graph to be displayed on home-page
        activity_json('static/activity-data.js')
