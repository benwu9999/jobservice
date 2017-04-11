from __future__ import unicode_literals
from django.db import models
import uuid

# Create your models here.
class Jobpost(models.Model):
	"""
	data model for Jobpost
	"""
	jobPostId=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        at=models.DateTimeField(auto_now=True,null=True)
        asof=models.DateTimeField(null=True)
        title=models.CharField(max_length=200, null=True)
        description=models.CharField(max_length=200, null=True)
        employerProfileId=models.CharField(max_length=200, null=True)
        locationId=models.CharField(max_length=200, null=True)

class Compensation(models.Model):
	"""
	data model for compensation information
	"""
        compensationId=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        amount=models.IntegerField(default=0, null=True)
        duration=models.CharField(max_length=200, null=True)
        jobpost=models.ForeignKey(Jobpost,related_name='compensation', null=True, on_delete=models.CASCADE)
