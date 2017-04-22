
from  django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns=[
	url(r'^$', views.index, name='index'),
	url(r'^jobPost/$', views.JobPostList.as_view()), # need the '/' before $
	# the () will capture the last element of the url as pass it as a parameter to the view function
	url(r'^jobPost/(.*)$', views.JobPostDetail.as_view()),

	url(r'^jobPost/allIds$',views.AllIdsList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
