import logging

from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'This command invoke all the importing data command'

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        try:
            call_command('import_organization_data')
        except Exception as ex:
            logger.error(ex)
        try:
            call_command('import_affiliated_committers_data')
        except Exception as ex:
            logger.error(ex)
        try:
            call_command('import_outside_committers_data')
        except Exception as ex:
            logger.error(ex)
        try:
            call_command('import_outside_projects_data')
        except Exception as ex:
            logger.error(ex)
        try:
            call_command('import_portfolio_projects_data')
        except Exception as ex:
            logger.error(ex)
            return
        logger.info('All OpenHub data is imported')
