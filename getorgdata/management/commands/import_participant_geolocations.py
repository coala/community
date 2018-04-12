from django.core.management.base import BaseCommand

from getorgdata.get_geolocation import import_data, org_location_dict


class Command(BaseCommand):
    help = 'Import Participant GeoLocation'

    ORG_LOCATION_DICT = staticmethod(org_location_dict)
    IMPORT_DATA = staticmethod(import_data)

    def handle(self, *args, **options):
        for key, value in self.ORG_LOCATION_DICT.items():
            self.IMPORT_DATA(self, key, value)
