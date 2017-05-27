from __future__ import unicode_literals
from django.db import models
import uuid
from django.contrib.auth.models import User
from JobPostService.job_post_app.models import JobPost

class Application(models.Model):
    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='user',
        null=True,
        blank=True
    )
    job_post = models.ForeignKey(
        JobPost,
        on_delete=models.SET_NULL,
        related_name='job_post',
        null=True,
        blank=True
    )
    status = models.CharField(max_length=10)
