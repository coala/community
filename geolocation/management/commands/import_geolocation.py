from github import Github
import getorg

# Get an API key (for just querying, give it no write permissions) at https://github.com/settings/tokens
from community.settings import gh_key
# You can leave login_or_token blank, but then you only get 60 queries an hour
gh = Github(login_or_token=gh_key)

from geolocation.models import Participant
from django.core.management.base import BaseCommand
from geoposition import Geoposition
from community.git import get_owner

org_name =get_owner()
map, org_location_dict, org_metadata_dict = getorg.orgmap.map_orgs(gh,org_name)


class Command(BaseCommand):
    def import_data(self, key, value):
        name = key
        position = Geoposition(value[1][0], value[1][1])

        try:
            c, created = Participant.objects.get_or_create(
                name = name,
                position = position
            )
            if created:
                c.save()
                print ("\nContributor, {}, has been saved.".format(c))
        except Exception as ex:
            print ("\n\nSomething went wrong saving this contributor: {}\n{}".format(name, str(ex)))


    def handle(self, *args, **options):
        """
        Makes a GET request to the  API.
        """
        for key, value in org_location_dict.items():
        	self.import_data(key, value)
