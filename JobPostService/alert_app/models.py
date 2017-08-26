from __future__ import unicode_literals
from django.db import models
import uuid
from django_unixdatetimefield import UnixDateTimeField


class AlertConfig(models.Model):
    alert_config_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = UnixDateTimeField(null=True, blank=True)
    modified = UnixDateTimeField(auto_now=True)
