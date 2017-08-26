from  django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^alert/$', views.AlertConfigList.as_view()),
    url(r'^alert/(?P<alertConfigId>.+)$', views.AlertConfigDetail.as_view()),
    url(r'^alert?userId=', views.AlertConfigByUserId.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
