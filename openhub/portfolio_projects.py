import logging

from community.git import get_org_name
from openhub.models import PortfolioProject, PortfolioProjectActivity


def get_portfolio_projects_data(json_object):
    data = json_object['response']['result'
                                   ]['portfolio_projects']['project']
    return data


def import_data(project):
    logger = logging.getLogger(__name__)
    name = project.get('name', None)

    try:
        (cr, create) = PortfolioProjectActivity.objects.get_or_create(
            **project['twelve_mo_activity_and_year_on_year_change']
            )
        if create:
            cr.save()
            project['twelve_mo_activity_and_year_on_year_change'] = cr
            project['org'] = get_org_name()
        (c, created) = PortfolioProject.objects.get_or_create(
            **project
            )
        if created:
            c.save()
            logger.info('\nPortfolioProject %s has been saved' % name)
    except Exception as ex:
        logger.error(
            'Something went wrong saving this PortfolioProject %s: %s'
            % (name, ex))
