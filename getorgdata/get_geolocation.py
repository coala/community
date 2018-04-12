from github import Github
import getorg
import logging

from getorgdata.gh_token import GH_TOKEN
from getorgdata.models import Participant, Getorg
from geoposition import Geoposition
from community.git import get_org_name

gh = Github(login_or_token=GH_TOKEN)
map, org_location_dict, org_metadata_dict = getorg.orgmap.map_orgs(
    gh, get_org_name())


def import_data(self, key, value):
    name = key
    logger = logging.getLogger(__name__)
    try:
        position = Geoposition(value[1][0], value[1][1])
    except Exception as ex:
        logger.error(ex)

    try:
        (cr, create) = Getorg.objects.get_or_create(
            org_name=get_org_name()
            )
        if create:
            cr.save()
        c, created = Participant.objects.get_or_create(
            org_name=cr,
            name=name,
            position=position
        )
        if created:
            c.save()
            logger.info('GeoLocation of %s has been saved' % c)
    except Exception as ex:
        logger.error(
            'Something went wrong saving the GeoLocation of Participant %s: %s'
            % (name, ex))
