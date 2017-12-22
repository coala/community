from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
import logging

from community.git import get_owner


def index(request):
    logger = logging.getLogger(__name__)
    logger.info('this package is alive')
    org_twitter_handle = org_name = get_owner()
    api_data_dump = json.loads(
        requests.get('https://gci-leaders.netlify.com/data.json').content)
    for item in api_data_dump:
        if item['name'] == org_name:
            org_twitter_handle = item['twitter_url'].split(
                'twitter.com/')[-1]
    org_data = {
        'org_twitter_handle': org_twitter_handle
    }
    if org_twitter_handle is not None:
        return render(request, 'twitter_feed.html', context=org_data)
    else:
        return HttpResponse("Sorry, Organisation's twitter handle not found!")
