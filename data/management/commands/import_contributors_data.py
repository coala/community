from django.core.management.base import BaseCommand

from data.contrib_data import get_contrib_data, import_data


class Command(BaseCommand):
    help = 'Import Contributors Data'

    CONTRIBUTORS = staticmethod(get_contrib_data)
    IMPORT_DATA = staticmethod(import_data)

    def handle(self, *args, **options):
        for contributor in self.CONTRIBUTORS():
            self.IMPORT_DATA(contributor)
