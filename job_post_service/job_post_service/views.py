# Create your views here.
import logging

from django.http import HttpResponse

from serializers import JobPostSerializer


def index(request):
    return HttpResponse("Hello World! This is our Test App.")


from rest_framework import generics
from models import JobPost
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

# uncomment the line below if you want to enable csrf protection for this view
#@method_decorator(csrf_protect, name='post')
class JobPostList(generics.ListCreateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer


class JobPostDetail(generics.RetrieveUpdateDestroyAPIView):

    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'jobPostId'
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer


class AllIdsList(APIView):
    """
    Return a list of jobPostIds
    """

    def get(self, request, format=None):
        allIdList = sorted([x['jobPostId'] for x in JobPost.objects.values('jobPostId')])
        return Response(data=allIdList)
