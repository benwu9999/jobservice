# Create your views here.
import logging

from django.db.models import Q
from django.http import HttpResponse


def index(request):
    return HttpResponse("application service api")


from rest_framework import generics, status
from models import Alert, Query, MONTHLY, WEEKLY, DAILY
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import AlertSerializer

logger = logging.getLogger(__name__)


class AlertConfigList(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def post(self, request, *args, **kwargs):
        alert_d = request.data
        # alert_d['employer_profile_id'] = alert_d.pop('employer_profile')['profile_id']
        # alert_d['location_id'] = alert_d.pop('location')['location_id']
        if 'alert_id' not in alert_d:
            okStatus = status.HTTP_201_CREATED
        else:
            okStatus = status.HTTP_200_OK

        alert_d['query']['terms'] = ','.join(alert_d['query']['terms'])
        alert_d['query']['employer_names'] = ','.join(alert_d['query']['employer_names'])
        alert_d['query']['locations'] = ','.join(alert_d['query']['locations'])
        query = Query(**alert_d.pop('query'))
        query.save()

        alert_d['query'] = query

        alert = Alert(**alert_d)
        alert.save()

        return Response(AlertSerializer(alert).data, status=okStatus)


class AlertConfigDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

class AlertSearchByIds(APIView):
    permission_classes = ()

    def get(self, request, format=None):
        if 'ids' in request.query_params:
            q = Q(pk__in=request.query_params['ids'].split(','))
            z = AlertSerializer(Alert.objects.filter(q), many=True)
            return Response(z.data)
        return Response([])


class AlertFreqList(APIView):
    frequencies = [DAILY, WEEKLY, MONTHLY];

    def get(self, request, format=None):
        return Response(AlertFreqList.frequencies)
