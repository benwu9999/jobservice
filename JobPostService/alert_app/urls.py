from  django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^jobPostAlert/alertFreq$', views.AlertFreqList.as_view()),
    url(r'^jobPostAlert$', views.AlertConfigList.as_view()),
    url(r'^jobPostAlert/ids', views.AlertSearchByIds.as_view()),
    url(r'^jobPostAlert/generateEmail', csrf_exempt(views.GenerateEmail.as_view())),
    url(r'^jobPostAlert/(?P<pk>.+)$', views.AlertConfigDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
