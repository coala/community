import logging

from community.git import get_org_name
from openhub.models import MostCommit, MostRecentCommit, AffiliatedCommitter


def get_affiliated_committers_data(json_object):
    data = json_object['response']['result'
                                   ]['affiliated_committers']['affiliator']
    return data


def import_data(affiliator):
    logger = logging.getLogger(__name__)
    name = affiliator.get('name', None)

    try:
        (cr1, create1) = MostCommit.objects.get_or_create(
            **affiliator['most_commits']
            )
        if create1:
            cr1.save()
        (cr2, create2) = MostRecentCommit.objects.get_or_create(
            **affiliator['most_recent_commit']
            )
        if create2:
            cr2.save()
        affiliator['most_commits'] = cr1
        affiliator['most_recent_commit'] = cr2
        affiliator['org'] = get_org_name()
        (c, created) = AffiliatedCommitter.objects.get_or_create(
            **affiliator
            )
        if created:
            c.save()
            logger.info(
                '\nAffiliatedCommitter %s has been saved' % c)
    except Exception as ex:
        logger.error(
            '\n\nSomething went wrong saving this AffiliatedCommitter %s: %s'
            % (name, ex))
