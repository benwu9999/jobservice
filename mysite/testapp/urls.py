
from  django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns=[
	url(r'^$', views.index, name='index'),
	url(r'^jobPost/$',views.JobpostList.as_view()),
	url(r'^jobPost/(?P<pk>[0-9a-f-]+)/$', views.JobpostDetail.as_view()),
	url(r'^jobPost/allIds/$',views.AllIdsList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
