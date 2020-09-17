import os
import json

import logging

import getorg

from data.models import Contributor


def handle(output_dir='cluster_map'):
    """
    Creates a organization cluster map using the contributors location
    stored in the database
    :param output_dir: Directory where all the required CSS and JS files
    are copied by 'getorg' package
    """
    logger = logging.getLogger(__name__)
    logger.info("'cluster_map/' is the default directory for storing"
                " organization map related files. If arg 'output_dir'"
                ' not provided it will be used as a default directory by'
                " 'getorg' package.")

    # For creating the organization map, the 'getorg' uses a 'Nominatim' named
    # package which geocodes the contributor location and then uses that class
    # to create the map. Since, we're not dealing with that function which use
    # that 'Nominatim' package because we're fetching a JSON data and storing
    # it in our db. Therefore, defining our own simple class that can aid us
    # to create a cluster map.
    class Location:

        def __init__(self, longitude, latitude):
            self.longitude = longitude
            self.latitude = latitude

    org_location_dict = {}

    for contrib in Contributor.objects.filter(location__isnull=False):
        user_location = json.loads(contrib.location)
        location = Location(user_location['longitude'],
                            user_location['latitude'])
        org_location_dict[contrib.login] = location
        logger.debug(f'{contrib.login} location {user_location} added on map')
    getorg.orgmap.output_html_cluster_map(org_location_dict,
                                          folder_name=output_dir)

    move_and_make_changes_in_files(output_dir)


def move_and_make_changes_in_files(output_dir):
    """
    Move static files from 'output_dir' to django static folder which
    is being required by the map.html which is being auto-generated
    by getorg.
    :param output_dir: Directory from where the files have to be moved
    """

    move_leaflet_dist_folder(output_dir)

    os.rename(
        src=get_file_path(os.getcwd(), output_dir, 'org-locations.js'),
        dst=get_file_path(os.getcwd(), 'static', 'org-locations.js')
    )

    os.remove(get_file_path(os.getcwd(), output_dir, 'map.html'))


def move_leaflet_dist_folder(output_dir):
    source_path = get_file_path(os.getcwd(), output_dir, 'leaflet_dist')
    destination_path = get_file_path(os.getcwd(), 'static', 'leaflet_dist')

    # Remove existing leaflet_dir if exists
    for root, dirs, files in os.walk(destination_path):
        for file in files:
            os.remove(os.path.join(destination_path, file))
        os.rmdir(root)

    os.renames(source_path, destination_path)


def get_file_path(*args):
    return '/'.join(args)
