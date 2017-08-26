# Create your views here.
import logging

import sys
from django.http import HttpResponse

from serializers import JobPostSerializer


def index(request):
    return HttpResponse("Hello World! This is our Test App.")


from rest_framework import generics, status
from models import JobPost
from rest_framework.response import Response
from rest_framework.views import APIView
import json

logger = logging.getLogger(__name__)


# asc = ApplicationServiceClient();
# usc = UserServiceClient();

# def unapplied_job_posts(self, user, page_from):
#     applied_job_posts = acs.application(user)
#     applied_job_post_ids = [x.job_post_id for x in applied_job_posts]
#     unapplied_job_posts = self.job_posts(not_in=applied_job_post_ids)
#     return unapplied_job_posts
#
#
# def job_posts(**kwargs):
#     rest_params = convert_to_rest_params(kwargs)
#     self.job_posts

# uncomment the line below if you want to enable csrf protection for this view
# @method_decorator(csrf_protect, name='post')
class JobPostList(generics.ListCreateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer

    def get(self, request, *args, **kwargs):
        if 'by' in request.data:
            profile_ids = request.data.pop('by').split(',')
            return JobPost.objects.filter(employer_profile_id__in=profile_ids)
        else:
            return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        job_post_data = request.data.pop('jobPost')
        job_post_data['employerProfileId'] = job_post_data['employerProfile']['profileId']
        job_post_data['locationId'] = job_post_data['location']['locationId']
        # request.data has user info, not using it for now
        job_post = JobPostSerializer(data=job_post_data)
        if job_post.is_valid():
            job_post.save()  # will call .create()
            return Response(job_post.data, status=status.HTTP_201_CREATED)
        else:
            return Response(job_post.errors, status=status.HTTP_400_BAD_REQUEST)


class JobPostDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'jobPostId'
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer


class JobPostSearch(APIView):
    def get(self, request, format=None):
        try:
            if 'by' in request.query_params:
                serializer = JobPostSerializer(JobPost.objects.filter(
                    pk__in=request.query_params['by'].split(',')), many=True)
                ret = {
                    'job_posts' : serializer.data,
                    'total_job_post_count' : len(serializer.data)
                }
                return Response(ret)
        except:
            return Response(sys.exc_info()[0])


class JobPostBulkSave(APIView):
    def post(self, request, format=None):
        data = request.data
        job_posts = data['jobPosts']
        JobPost.objects.bulk_create([JobPost(**json.loads(j)) for j in job_posts])
        return Response(len(job_posts))


class CompensationList(APIView):
    compensation = ['Hour', 'Day', 'Week', 'Month', 'Year'];

    def get(self, request, format=None):
        return Response(CompensationList.compensation)


class AllIdsList(APIView):
    """
    Return a list of jobPostIds
    """

    def get(self, request, format=None):
        allIdList = sorted([x['jobPostId'] for x in JobPost.objects.values('jobPostId')])
        return Response(data=allIdList)
