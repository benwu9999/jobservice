from __future__ import unicode_literals
from django.db import models
import uuid

# Create your models here.
class Compensation(models.Model):

    """
    data model for compensation information
    """
    class Meta:
        db_table = 'compensation'
        # unique_together = ("amount", "duration")

    compensationId=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount=models.IntegerField(default=0, null=True)
    duration=models.CharField(max_length=200, null=True)

class JobPost(models.Model):

    """
    data model for Job Post
    """
    class Meta:
        db_table = 'job_post'

    jobPostId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True)
    description=models.CharField(max_length=200, null=True)
    employerProfileId=models.CharField(max_length=200, null=True)
    locationId=models.CharField(max_length=200, null=True)
    at = models.DateTimeField(auto_now=True, null=True)
    compensation = models.ForeignKey(
        Compensation,
        on_delete=models.SET_NULL,
        related_name='compensation',
        null=True,
        blank=True
    )
