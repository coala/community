from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.GCIStudentsList.as_view(), name='index'),
]
