# Create your views here.
import logging

from django.http import HttpResponse


def index(request):
    return HttpResponse("application service api")


from rest_framework import generics
from models import AlertConfig
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import AlertConfigSerializer

logger = logging.getLogger(__name__)

class AlertConfigList(generics.ListCreateAPIView):
    queryset = AlertConfig.objects.all()
    serializer_class = AlertConfigSerializer

class AlertConfigDetail(generics.RetrieveUpdateDestroyAPIView):

    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'alert_config_id'
    queryset = AlertConfig.objects.all()
    serializer_class = AlertConfigSerializer

class AlertConfigByUserId(APIView):

    def get(self, request, format=None):
        alert_configs = AlertConfig.objects.filter(user_id = request.data['user_id'])
        return Response(alert_configs)