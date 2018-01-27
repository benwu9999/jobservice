from __future__ import unicode_literals

import datetime
import uuid

import dateutil.parser
import pytz
from django.db import models
from django.utils.timezone import make_aware
from django_unixdatetimefield import UnixDateTimeField

from admin_site.settings import TIME_ZONE
from job_post_app.models import Compensation

TIME_ZONE = pytz.timezone(TIME_ZONE)

class Query(models.Model):
    """
    location_id - the active location id of the user when this query is created

    profile_id - the active profile id of the user when this query is created

    commute - commute time in minutes
    """
    query_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terms = models.CharField(max_length=400, null=True)
    employer_names = models.CharField(max_length=400, null=True)
    commute = models.IntegerField(null=True)
    location_id = models.UUIDField(primary_key=False, null=True, editable=False)
    profile_id = models.UUIDField(primary_key=False, null=True, editable=False)
    locations = models.CharField(max_length=400, null=True)
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
    last_updated = UnixDateTimeField(null=True)
    created = UnixDateTimeField()
    modified = UnixDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        elif type(self.created) is str:
            self.created = dateutil.parser.parse(self.created)
        # self.last_updated = make_aware(dateutil.parser.parse(self.last_updated), is_dst=True)
        if self.last_updated:
            self.last_updated = dateutil.parser.parse(self.last_updated)
        super(Query, self).save()

    def last_updated_w_tz(self):
        return TIME_ZONE.localize(self.last_updated)


DAILY = 'Daily'
WEEKLY = 'Weekly'
MONTHLY = 'Monthly'

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
