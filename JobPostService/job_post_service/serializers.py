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
    compensation = CompensationSerializer(many=False)

    class Meta:
        model = JobPost
        fields = ('jobPostId', 'title', 'description', 'employerProfileId', 'locationId', 'compensation', 'at')

    def create(self, validated_data):
        compensation_data = validated_data.pop('compensation')
        compensation = Compensation.objects.create(**compensation_data)
        jobPost = JobPost.objects.create(compensation=compensation, **validated_data)
        self.is_valid(raise_exception=True)
        jobPost.save()
        return jobPost

    def update(self, instance, validated_data):
        compensation_data = validated_data.pop('compensation')
        compensation = instance.compensation

        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.employerProfileId = validated_data['employerProfileId']
        instance.locationId = validated_data['locationId']
        instance.save()
        
        compensation.amount = compensation_data['amount']
        compensation.duration = compensation_data['duration']
        compensation.save()

        return instance
