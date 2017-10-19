from  django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^jobPost/compensations$', views.CompensationList.as_view()),
    url(r'^jobPost/allIds$', views.AllIdsList.as_view()),
    url(r'^jobPost/search?', views.JobPostSearch.as_view()),

    # need the '/' before $ to properly route call to generics.ListCreateAPIView
    url(r'^jobPost$', views.JobPostList.as_view()),

    # supports /jobPost/{jobPostId}
    url(r'^jobPost/(?P<pk>.+)$', views.JobPostDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
