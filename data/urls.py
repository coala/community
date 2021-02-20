from django.conf.urls import url

from .views import ContributorsListView

urlpatterns = [
    url(r'^$', ContributorsListView.as_view(), name='index'),
]
