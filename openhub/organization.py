import json
import logging

import requests
import xmltodict

from community.git import get_org_name
from openhub.oh_token import OH_TOKEN
from openhub.models import InfographicDetail, Organization


def get_organization_data():
    import_url = ('https://www.openhub.net/orgs/'
                  + get_org_name() + '.xml?api_key=' + OH_TOKEN)
    resp = requests.get(import_url)
    jsonString = json.dumps(xmltodict.parse(resp.content), indent=4)
    json_object = json.loads(jsonString)
    jdict = json_object['response']['result']['org']
    data = json.dumps(jdict)
    org = json.loads(data)

    return org


def import_data(org):
    logger = logging.getLogger(__name__)
    name = org['name']

    try:
        (cr, create) = InfographicDetail.objects.get_or_create(
            **org['infographic_details']
            )
        if create:
            cr.save()
        org['infographic_details'] = cr
        org['org_type'] = org.pop('type')
        org.pop('portfolio_projects')
        org.pop('vanity_url')
        (c, created) = Organization.objects.get_or_create(
            **org
            )
        if created:
            c.save()
            logger.info('\nOrganization %s has been saved' % name)
    except Exception as ex:
        logger.error(
            'Something went wrong saving this Organization %s: %s'
            % (name, ex))
