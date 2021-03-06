from  django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^application$', views.ApplicationList.as_view()),
    url(r'^application/(?P<applicationId>.+)$', views.ApplicationDetail.as_view()),
    url(r'^application?userId=', views.ApplicationByUserId.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
