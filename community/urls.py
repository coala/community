"""
Community URL configuration.
"""

from django_distill import distill_url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from gci.views import index as gci_index
from gci.feeds import LatestTasksFeed as gci_tasks_rss
from gsoc.views import index as gsoc_index
from gsoc.views import projects as gsoc_projects
from activity.scraper import activity_json
from twitter.view_twitter import index as twitter_index
from log.view_log import index as log_index


def get_index():
    # The index URI regex, ^$, contains no parameters, named or otherwise.
    # You can simply just return nothing here.
    return None


urlpatterns = [
    distill_url(
        r'^$', TemplateView.as_view(template_name='index.html'),
        name='index',
        distill_func=get_index,
        distill_file='index.html',
    ),
    distill_url(
        r'static/activity-data.json', activity_json,
        name='activity_json',
        distill_func=get_index,
        distill_file='static/activity-data.json',
    ),
    distill_url(
        r'activity/', TemplateView.as_view(template_name='activity.html'),
        name='activity',
        distill_func=get_index,
        distill_file='activity/index.html',
    ),
    distill_url(
        r'gci/tasks/rss.xml', gci_tasks_rss(),
        name='gci-tasks-rss',
        distill_func=get_index,
        distill_file='gci/tasks/rss.xml',
    ),
    distill_url(
        r'gci/', gci_index,
        name='community-gci',
        distill_func=get_index,
        distill_file='gci/index.html',
    ),
    distill_url(
        r'^gsoc/$', gsoc_index,
        name='community-gsoc',
        distill_func=get_index,
        distill_file='gsoc/index.html',
    ),
    distill_url(
        r'^gsoc/projects/$', gsoc_projects,
        name='community-gsoc-projects',
        distill_func=get_index,
        distill_file='gsoc/projects.html',
    ),
    distill_url(
        r'twitter/', twitter_index,
        name='twitter',
        distill_func=get_index,
        distill_file='twitter/index.html',
    ),
    distill_url(
        r'log/', log_index,
        name='log',
        distill_func=get_index,
        distill_file='log/index.html',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
