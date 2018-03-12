from django.http import HttpResponse
import requests
import json
import logging

from community.git import get_org_name


def index(request):
    logger = logging.getLogger(__name__)
    logger.info('this package is alive')
    s = []

    org_twitter_handle = org_name = get_org_name()

    s.append('<link rel="shortcut icon" type="image/png" '
             'href="../static/favicon.png"/>')

    api_data_dump = json.loads(
        requests.get('https://gci-leaders.netlify.com/data.json').content)
    for item in api_data_dump:
        if item['name'] == org_name:
            org_twitter_handle = item['twitter_url'].split(
                'twitter.com/')[-1]
    if org_twitter_handle is not None:
        s.append('<a class="twitter-timeline" data-height="1000" '
                 'data-link-color="#2B7BB9" '
                 'href="https://twitter.com/{twitter_handle}">'
                 'Tweets by {twitter_handle}</a> <script async '
                 'src="https://platform.twitter.com/widgets.js" '
                 'charset="utf-8"></script>'.format(
                     twitter_handle=org_twitter_handle))

    return HttpResponse('\n'.join(s))
