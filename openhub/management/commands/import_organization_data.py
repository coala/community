import logging

from django.core.management.base import BaseCommand

from openhub.organization import get_organization_data, import_data


class Command(BaseCommand):
    help = 'Import Organization data'

    COLLECTIONS = staticmethod(get_organization_data)
    IMPORT_DATA = staticmethod(import_data)

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        try:
            self.IMPORT_DATA(self.COLLECTIONS())
        except Exception as ex:
            logger.error(ex)
            return
