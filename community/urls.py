"""
Community URL configuration.
"""
from django.conf.urls import url
from django.urls import include
from django_distill import distill_url
from django.conf.urls.static import static
from django.conf import settings

from community.views import HomePageView, JoinCommunityView
from gci.views import GCIStudentsList
from gci.feeds import LatestTasksFeed as gci_tasks_rss
from ci_build.view_log import BuildLogsView
from data.views import ContributorsListView
from gamification.views import GamificationResults
from meta_review.views import ContributorsMetaReview
from inactive_issues.inactive_issues_scraper import inactive_issues_json
from unassigned_issues.unassigned_issues_scraper import (
    unassigned_issues_activity_json,
)


def get_index():
    # The index URI regex, ^$, contains no parameters, named or otherwise.
    # You can simply just return nothing here.
    return None


urlpatterns = [
    distill_url(
        r'^$', HomePageView.as_view(),
        name='index',
        distill_func=get_index,
        distill_file='index.html',
    ),
    distill_url(
        r'^join/', JoinCommunityView.as_view(),
        name='join-community',
        distill_func=get_index,
        distill_file='join/index.html',
    ),
    distill_url(
        r'gci/tasks/rss.xml', gci_tasks_rss(),
        name='gci-tasks-rss',
        distill_func=get_index,
        distill_file='gci/tasks/rss.xml',
    ),
    distill_url(
        r'gci/', GCIStudentsList.as_view(),
        name='community-gci',
        distill_func=get_index,
        distill_file='gci/index.html',
    ),
    distill_url(
        r'ci/build/', BuildLogsView.as_view(),
        name='ci_build',
        distill_func=get_index,
        distill_file='ci/build/index.html',
    ),
    distill_url(
        r'contributors/$', ContributorsListView.as_view(),
        name='community-data',
        distill_func=get_index,
        distill_file='contributors/index.html',
    ),
    distill_url(
        r'meta-review/$', ContributorsMetaReview.as_view(),
        name='meta_review_data',
        distill_func=get_index,
        distill_file='meta-review/index.html',
    ),
    distill_url(
        r'static/inactive-issues.json', inactive_issues_json,
        name='inactive_issues_json',
        distill_func=get_index,
        distill_file='static/inactive-issues.json',
    ),
    distill_url(
        r'static/unassigned-issues.json', unassigned_issues_activity_json,
        name='unassigned_issues_activity_json',
        distill_func=get_index,
        distill_file='static/unassigned-issues.json',
    ),
    distill_url(
        r'gamification/$', GamificationResults.as_view(),
        name='community-gamification',
        distill_func=get_index,
        distill_file='gamification/index.html',
    ),
    url(r'openhub/', include('openhub.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
