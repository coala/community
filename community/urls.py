"""
Community URL configuration.
"""

from django_distill import distill_url

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
]
