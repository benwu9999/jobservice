
from  django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns=[
	url(r'^$', views.index, name='index'),

	# need the '/' before $ to properly route call to generics.ListCreateAPIView
	url(r'^jobPost/$', views.JobPostList.as_view()),

	# supports /jobPost/{jobPostId}
	url(r'^jobPost/(?P<jobPostId>.+)$', views.JobPostDetail.as_view()),

	url(r'^jobPost/allIds$',views.AllIdsList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
