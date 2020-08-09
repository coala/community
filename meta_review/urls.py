from django.conf.urls import url

from .views import ContributorsMetaReview

urlpatterns = [
    url(r'^$', ContributorsMetaReview.as_view(), name='index'),
]
