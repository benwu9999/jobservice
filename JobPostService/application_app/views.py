# Create your views here.
import logging

from django.http import HttpResponse

def index(request):
    return HttpResponse("application service api")


from rest_framework import generics
from models import Application
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import ApplicationSerializer

logger = logging.getLogger(__name__)

class ApplicationList(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):

    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'application_id'
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class ApplicationByUserId(APIView):

    def get(self, request, format=None):
        applications = Application.objects.filter(user_id = request.data['user_id'])
        return Response(applications)