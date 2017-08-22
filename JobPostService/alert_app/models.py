from __future__ import unicode_literals
from django.db import models
import uuid
from django.contrib.auth.models import User

class AlertConfig(models.Model):
    alert_config_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
