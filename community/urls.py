"""
Community URL configuration.
"""

from django_distill import distill_url
from django.conf.urls.static import static
from django.conf import settings

from community.views import HomePageView
from gci.views import index as gci_index
from gci.feeds import LatestTasksFeed as gci_tasks_rss
from ci_build.view_log import BuildLogsView
from data.views import index as contributors_index
from gamification.views import index as gamification_index
from meta_review.views import index as meta_review_index
from inactive_issues.inactive_issues_scraper import inactive_issues_json
from openhub.views import index as openhub_index
from model.views import index as model_index
from openhub.models import (
    PortfolioProject,
    OutsideCommitter,
    AffiliatedCommitter,
    OutsideProject,
    Organization,
    )
from model.views import (
    PortfolioProjectListView,
    PortfolioProjectDetailView,
    AffiliatedCommitterListView,
    AffiliatedCommitterDetailView,
    OrganizationListView,
    OrganizationDetailView,
    OutsideProjectListView,
    OutsideProjectDetailView,
    OutsideCommitterListView,
    OutsideCommitterDetailView,
    )
from unassigned_issues.unassigned_issues_scraper import (
    unassigned_issues_activity_json,
)


def get_index():
    # The index URI regex, ^$, contains no parameters, named or otherwise.
    # You can simply just return nothing here.
    return None


def get_all_portfolioprojects():
    for portfolioproject in PortfolioProject.objects.all():
        yield {'pk': portfolioproject.id}


def get_all_outsidecommitters():
    for outsidecommitter in OutsideCommitter.objects.all():
        yield {'pk': outsidecommitter.id}


def get_all_outsideprojects():
    for outsideproject in OutsideProject.objects.all():
        yield {'pk': outsideproject.id}


def get_all_affiliatedcommitters():
    for affiliatedcommitter in AffiliatedCommitter.objects.all():
        yield {'pk': affiliatedcommitter.id}


def get_organization():
    for organization in Organization.objects.all():
        yield {'pk': organization.id}


urlpatterns = [
    distill_url(
        r'^$', HomePageView.as_view(),
        name='index',
        distill_func=get_index,
        distill_file='index.html',
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
        r'ci/build/', BuildLogsView.as_view(),
        name='ci_build',
        distill_func=get_index,
        distill_file='ci/build/index.html',
    ),
    distill_url(
        r'contributors/$', contributors_index,
        name='community-data',
        distill_func=get_index,
        distill_file='contributors/index.html',
    ),
    distill_url(
        r'meta-review/$', meta_review_index,
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
        r'openhub/$', openhub_index,
        name='community-openhub',
        distill_func=get_index,
        distill_file='openhub/index.html',
    ),
    distill_url(
        r'model/$', model_index,
        name='community-model',
        distill_func=get_index,
        distill_file='model/index.html',
    ),
    distill_url(
        r'model/openhub/outside_committers/$',
        OutsideCommitterListView.as_view(),
        name='outsidecommitters',
        distill_func=get_index,
    ),
    distill_url(
        r'model/openhub/outside_committer/(?P<pk>\d+)/$',
        OutsideCommitterDetailView.as_view(),
        name='outsidecommitter-detail',
        distill_func=get_all_outsidecommitters,
    ),
    distill_url(
        r'model/openhub/outside_projects/$',
        OutsideProjectListView.as_view(),
        name='outsideprojects',
        distill_func=get_index,
    ),
    distill_url(
        r'model/openhub/outside_project/(?P<pk>\d+)/$',
        OutsideProjectDetailView.as_view(),
        name='outsideproject-detail',
        distill_func=get_all_outsideprojects,
    ),
    distill_url(
        r'model/openhub/affiliated_committers/$',
        AffiliatedCommitterListView.as_view(),
        name='affiliatedcommitters',
        distill_func=get_index,
    ),
    distill_url(
        r'model/openhub/affiliated_committer/(?P<pk>\d+)/$',
        AffiliatedCommitterDetailView.as_view(),
        name='affiliatedcommitter-detail',
        distill_func=get_all_affiliatedcommitters,
    ),
    distill_url(
        r'model/openhub/portfolio_projects/$',
        PortfolioProjectListView.as_view(),
        name='portfolioprojects',
        distill_func=get_index,
    ),
    distill_url(
        r'model/openhub/portfolio_project/(?P<pk>\d+)/$',
        PortfolioProjectDetailView.as_view(),
        name='portfolioproject-detail',
        distill_func=get_all_portfolioprojects,
    ),
    distill_url(
        r'model/openhub/organization/$',
        OrganizationListView.as_view(),
        name='organization',
        distill_func=get_index,
    ),
    distill_url(
        r'model/openhub/org/(?P<pk>\d+)/$',
        OrganizationDetailView.as_view(),
        name='org-detail',
        distill_func=get_organization,
    ),
    distill_url(
        r'static/unassigned-issues.json', unassigned_issues_activity_json,
        name='unassigned_issues_activity_json',
        distill_func=get_index,
        distill_file='static/unassigned-issues.json',
    ),
    distill_url(
        r'gamification/$', gamification_index,
        name='community-gamification',
        distill_func=get_index,
        distill_file='gamification/index.html',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
