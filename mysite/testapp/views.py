from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello World! This is our Test App.")

from rest_framework import generics
from testapp.models import Jobpost, Compensation
from testapp.serializers import JobpostSerializer, CompensationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status

class JobpostList(APIView):

	def get(self, request, format=None):
		querysets = Jobpost.objects.values()
		comp_list = Compensation.objects.values()
		comp_map = {x['jobpost_id']:x for x in comp_list}
		for x in querysets:
			x.update({'compensation':{'amount':comp_map[x['jobPostId']]['amount'],'duration':comp_map[x['jobPostId']]['duration']}})
		queryset = [x for x in querysets]
		serializer = JobpostSerializer(queryset, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = JobpostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class JobpostDetail(APIView):
	def get_object(self,pk):
	    try:
               return Jobpost.objects.values().get(pk=pk)
	    except Jobpost.DoesNotExist:
                raise Http404
	def get(self, request, pk, format=None):
	    queryset = self.get_object(pk=pk)
	    comp = Compensation.objects.values('amount','duration').get(jobpost_id=pk)
	    queryset.update({'compensation':comp})
	    serializer = JobpostSerializer(data=queryset)
	    serializer.is_valid()
	    return Response(serializer.data)

	def put(self,request, pk, format=None):
	    jobpost = self.get_object(pk=pk)
	    comp = Compensation.objects.values('amount','duration').get(jobpost_id=pk)
            jobpost.update({'compensation':{'amount':comp['amount'],'duration':comp['duration']}})
            serializer = JobpostSerializer(jobpost,data=request.data)
	    if serializer.is_valid():
		serializer.save()
 		return Response(serializer.data)
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self,request, pk, format=None):
	    jobpost = Jobpost.objects.get(pk=pk)
	    jobpost.delete()
	    return Response(status=status.HTTP_204_NO_CONTENT)
