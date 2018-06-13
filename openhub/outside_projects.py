import logging

from community.git import get_org_name
from openhub.models import OutsideProject
from openhub.checker import data_checker


def get_outside_projects_data(json_object):
    """
    :param json_object: json data of outside projects
    :return: a list of outside projects dict
    """
    data = json_object['response']['result'
                                   ]['outside_projects']['project']
    _data = data_checker(data)
    return _data


def import_data(project):
    logger = logging.getLogger(__name__)
    name = project.get('name', None)

    try:
        project['org'] = get_org_name()
        (c, created) = OutsideProject.objects.get_or_create(
            **project
            )
        if created:
            c.save()
            logger.info('\nOutsideProject %s has been saved' % c)
    except Exception as ex:
        logger.error(
            'Something went wrong saving this OutsideProject %s: %s'
            % (name, ex))
