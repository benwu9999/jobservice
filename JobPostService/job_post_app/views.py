# Create your views here.
import logging

import sys
import time

import operator

from datetime import datetime
from django.http import HttpResponse

from serializers import JobPostSerializer
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return HttpResponse("job post service api")


from rest_framework import generics, status
from models import JobPost, Compensation
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

    def post(self, request, *args, **kwargs):
        job_post_data = request.data.pop('job_post')
        job_post_data['employer_profile_id'] = job_post_data.pop('employer_profile')['profile_id']
        job_post_data['location_id'] = job_post_data.pop('location')['location_id']
        if 'job_post_id' not in job_post_data:
            okStatus = status.HTTP_201_CREATED
        else:
            okStatus = status.HTTP_200_OK

        compensation = Compensation(**job_post_data['compensation'])
        compensation.save()

        job_post_data['compensation'] = compensation

        jobPost = JobPost(**job_post_data)
        jobPost.save()

        return Response(JobPostSerializer(jobPost).data, status=okStatus)


class JobPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer


class JobPostSearch(APIView):
    def get(self, request, format=None):
        try:
            page_size = request.query_params['pageSize']
            qs = list()
            if 'employerProfileIds' in request.query_params:
                qs.append(Q(employer_profile_id__in=request.query_params['employerProfileIds'].split(',')))
            if 'locationIds' in request.query_params:
                qs.append(Q(location_id__in=request.query_params['locationIds'].split(',')))
            if 'ids' in request.query_params:
                qs.append(Q(pk__in=request.query_params['ids'].split(',')))
            if 'within' in request.query_params:
                qs.append(Q(created__gt=self.get_epoch(request.query_params['within'])))
            if 'has' in request.query_params:
                text_qs = list()
                text_qs.append(Q(**{'title__icontains': request.query_params['has']}))
                text_qs.append(Q(**{'description__icontains': request.query_params['has']}))
                qs.append(reduce(operator.or_, text_qs))

            if qs:
                job_posts = JobPost.objects.filter(reduce(operator.and_, qs))
            else:
                job_posts = JobPost.objects.all()
            if 'page' in request.query_params:
                try:
                    page = int(request.query_params['page'])
                    paginator = Paginator(job_posts, page_size)
                    job_posts = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    job_posts = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), return empty list
                    job_posts = []
            z = JobPostSerializer(job_posts, many=True)
            ret = {
                'job_posts': z.data,
                'job_post_count_for_search': paginator.count
            }
            return Response(ret)
        except:
            return Response(sys.exc_info()[0])

    def get_epoch(self, epoch):
        return int(time.time()) - epoch


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
