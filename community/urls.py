"""
Community URL configuration.
"""

from django_distill import distill_url
from django.conf.urls.static import static
from django.conf import settings
from gci.views import index


def get_index():
    # The index URI regex, ^$, contains no parameters, named or otherwise.
    # You can simply just return nothing here.
    return None


urlpatterns = [
    distill_url(
        r'^$', index,
        name='community-gci',
        distill_func=get_index,
        distill_file='index.html',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
