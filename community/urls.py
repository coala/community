"""
Community URL configuration.
"""

from django_distill import distill_url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from gci.views import index as gci_index
from twitter.view_twitter import index as twitter_index


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
        r'activity/', TemplateView.as_view(template_name='activity.html'),
        name='activity',
        distill_func=get_index,
        distill_file='activity/index.html',
    ),
    distill_url(
        r'gci/', gci_index,
        name='community-gci',
        distill_func=get_index,
        distill_file='gci/index.html',
    ),
    distill_url(
        r'twitter/', twitter_index,
        name='twitter',
        distill_func=get_index,
        distill_file='twitter/index.html',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
