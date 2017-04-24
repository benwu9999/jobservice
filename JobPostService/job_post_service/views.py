# Create your views here.
from django.http import HttpResponse
from django.core import serializers
from serializers import JobPostSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

import logging

def index(request):
    return HttpResponse("Hello World! This is our Test App.")


from rest_framework import generics, status
from models import JobPost, Compensation
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

logger = logging.getLogger(__name__)
# class JobPostList(APIView):
#     """
#     get:
#     Return a list of jobPosts
#
#     post:
#     Create a new job post instance
#     """
#
#     def get(self, request, format=None):
#         querysets = JobPost.objects.values()
#         comp_list = Compensation.objects.values()
#         comp_map = {x['jobpost_id']: x for x in comp_list}
#         for x in querysets:
#             x.update({'compensation': comp_map[x['jobPostId']]})
#         serializer = JobpostSerializer(querysets, many=True)
#         return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = JobpostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@method_decorator(csrf_protect, name='post')
class JobPostList(generics.ListCreateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer


class JobPostDetail(generics.RetrieveUpdateDestroyAPIView):

    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'jobPostId'
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer

# class JobPostList(APIView):
#     def post(self, request, format=None):
#         return HttpResponse('This is POST request')

# class JobPostDetail(APIView):
#     """
#     get:
#     Return a jobPost instance
#
#     put:
#     Modify a jobPost instance
#
#     delete:
#     remove the jobPost instance
#     """
#
#     def post(self, request, format=None):
#         serializer = JobPostSerializer(data=request)
#         return HttpResponse('This is POST request')
#
#     def get(self, request, id, format=None):
#         jobpost = self.get_object(id)
#         json = serializers.serialize("json", jobpost)
#         return Response(json)
#
#     def get_object(self, pk):
#         try:
#             jobpost = JobPost.objects.values().get(pk=pk)
#             comp = Compensation.objects.values('amount', 'duration').get(jobpost_id=pk)
#             jobpost.update({'compensation': comp})
#             return jobpost
#         except JobPost.DoesNotExist:
#             raise Http404
#
#     def put(self, request, pk, format=None):
#         jobpost = self.get_object(pk=pk)
#         serializer = JobPostSerializer(jobpost, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         jobpost = JobPost.objects.get(pk=pk)
#         jobpost.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class AllIdsList(APIView):
    """
    Return a list of jobPostIds
    """

    def get(self, request, format=None):
        allIdList = sorted([x['jobPostId'] for x in JobPost.objects.values('jobPostId')])
        return Response(data=allIdList)
