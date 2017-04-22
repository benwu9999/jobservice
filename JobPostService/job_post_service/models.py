from __future__ import unicode_literals
from django.db import models
import uuid

# Create your models here.
class JobPost(models.Model):
    jobPostId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True)
    description=models.CharField(max_length=200, null=True)
    employerProfileId=models.CharField(max_length=200, null=True)
    locationId=models.CharField(max_length=200, null=True)
    at = models.DateTimeField(auto_now=True, null=True)

class Compensation(models.Model):
    """
    data model for compensation information
    """
    compensationId=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount=models.IntegerField(default=0, null=True)
    duration=models.CharField(max_length=200, null=True)
    jobpost=models.ForeignKey(JobPost, related_name='compensation', null=True, on_delete=models.CASCADE)
