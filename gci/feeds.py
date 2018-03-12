import os.path
from ruamel.yaml import YAML
import markdown2
import dateutil.parser

from django.contrib.syndication.views import Feed
from community.git import get_deploy_url, get_org_name


class LatestTasksFeed(Feed):
    title = 'GCI tasks feed'
    link = get_deploy_url() + '/gci/tasks/rss.xml'
    description = 'GCI tasks ordered by modification time.'
    author_name = get_org_name()
    author_link = get_deploy_url()

    def items(self):
        yaml = YAML()
        with open(os.path.join('_site', 'tasks.yaml')) as f:
            res = list(yaml.load(f).values())

        res.sort(key=lambda x: x['last_modified'], reverse=True)

        return res

    def item_title(self, item):
        return item['name']

    def item_description(self, item):
        desc = item['description']
        if item['external_url']:
            desc += '\n\nExternal URL: [{url}]({url})'.format(
                url=item['external_url'])
        return markdown2.markdown(desc)

    def item_link(self, item):
        return 'https://codein.withgoogle.com/tasks/' + str(item['id'])

    def item_pubdate(self, item):
        return dateutil.parser.parse(item['last_modified'])

    def item_updateddate(self, item):
        return dateutil.parser.parse(item['last_modified'])

    def item_author_name(self):
        return self.author_name

    def item_categories(self, item):
        return tuple(item['tags'])
