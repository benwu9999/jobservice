from __future__ import unicode_literals
from django.db import models
import uuid
from django_unixdatetimefield import UnixDateTimeField
import datetime
import dateutil.parser

from job_post_app.models import Compensation


class Query(models.Model):
    query_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terms = models.CharField(max_length=400)
    employer_names = models.CharField(max_length=400)
    commute_hour = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    locations = models.CharField(max_length=400)
    shows_contact = models.BooleanField()
    min_comp = models.ForeignKey(
        Compensation,
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        blank=True
    )
    max_comp = models.ForeignKey(
        Compensation,
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        blank=True
    )
    last_updated = UnixDateTimeField()
    created = UnixDateTimeField()
    modified = UnixDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        elif type(self.created) is str:
            self.created = dateutil.parser.parse(self.created)
        self.last_updated = dateutil.parser.parse(self.last_updated)
        super(Query, self).save()


class Alert(models.Model):
    alert_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    frequency = models.CharField(max_length=200)
    query = models.ForeignKey(
        Query,
        on_delete=models.SET_NULL,
        related_name='alerts',
        null=True,
        blank=True
    )
    created = UnixDateTimeField()
    modified = UnixDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.created = dateutil.parser.parse(self.created)
        super(Alert, self).save()
