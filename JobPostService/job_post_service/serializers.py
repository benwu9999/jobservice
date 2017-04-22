from rest_framework import serializers
from models import JobPost, Compensation


class CompensationSerializer(serializers.ModelSerializer):
    """
    Serializer to convert Compensation object data to primitive Python Data types
    """

    class Meta:
        model = Compensation
        fields = ('amount', 'duration')


class JobPostSerializer(serializers.ModelSerializer):
    """
    Serializer to conver JobPost object data to primitive Python Data types
    """
    # compensationSerializer = CompensationSerializer()

    class Meta:
        model = JobPost
        fields = ('jobPostId', 'title', 'description', 'employerProfileId', 'locationId', 'compensation', 'at')

    def create(self, validated_data):
        # compensation_data = validated_data.pop('compensation')
        jobPost = JobPost.objects.create(**validated_data)
        self.is_valid(raise_exception=True)
        jobPost.save()
        # Compensation.objects.create(jobpost=jobpost, **compensation_data)
        # validated_data.update({'compensation': compensation_data})
        # validated_data.update({'at': jobpost.at})
        # validated_data.update({'jobPostId': jobpost.jobPostId})
        # return validated_data

    def update(self, jobPost, validated_data):
        # instance.update(validated_data)

        # compensation_data = validated_data.pop('compensation')
        # compensation = Compensation.objects.get(jobpost_id=instance['jobPostId'])
        # compensation.amount = compensation_data['amount']
        # compensation.duration = compensation_data['duration']

        jobPost.at = validated_data['at']
        jobPost.title = validated_data['title']
        jobPost.description = validated_data['description']
        jobPost.employerProfileId = validated_data['employerProfileId']
        jobPost.locationId = validated_data['locationId']
        jobPost.save()

        # compensation.save()

        return jobPost
