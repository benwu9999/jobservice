from rest_framework import serializers
from jobpostapp.models import Jobpost, Compensation

class CompensationSerializer(serializers.ModelSerializer):
	"""
	Serializer to convert Compensation object data to primitive Python Data types
	"""
	class Meta:
		model=Compensation
		fields=('amount','duration')

class JobpostSerializer(serializers.ModelSerializer):
	"""
	Serializer to conver Jobpost object data to primitive Python Data types
	"""
	compensation=CompensationSerializer()

	class Meta:
		model=Jobpost
		fields=('at','asof','jobPostId','title','description','employerProfileId','compensation','locationId')

	def create(self, validated_data):
	       	compensation_data=validated_data.pop('compensation')
	       	jobpost=Jobpost.objects.create(**validated_data)
	       	Compensation.objects.create(jobpost=jobpost, **compensation_data)
		validated_data.update({'compensation':compensation_data})
		validated_data.update({'at':jobpost.at})
		validated_data.update({'jobPostId':jobpost.jobPostId})
	       	return validated_data

        def update(self, instance, validated_data):
                instance.update(validated_data)

		compensation_data=validated_data.pop('compensation')
		compensation = Compensation.objects.get(jobpost_id=instance['jobPostId'])
	        compensation.amount=compensation_data['amount']
		compensation.duration=compensation_data['duration']	
		
		jobpost = Jobpost.objects.get(pk=instance['jobPostId'])		
		jobpost.asof=validated_data['asof']
                jobpost.title=validated_data['title']
                jobpost.description=validated_data['description']
                jobpost.employerProfileId=validated_data['employerProfileId']
                jobpost.locationId=validated_data['locationId']
		jobpost.save()

		compensation.save()

		return instance
