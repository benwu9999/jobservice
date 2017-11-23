from __future__ import unicode_literals
from django.db import models
import uuid
from django.contrib.auth.models import User
from django_unixdatetimefield import UnixDateTimeField

from job_post_app.models import JobPost

import datetime
import dateutil.parser


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
    created = UnixDateTimeField()
    modified = UnixDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.created = dateutil.parser.parse(self.created)
        super(Application, self).save()