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

    compensationId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.IntegerField(default=0, null=True)
    duration = models.CharField(max_length=200, null=True)


class JobPost(models.Model):
    """
    data model for Job Post
    """

    class Meta:
        db_table = 'job_post'

    jobPostId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    employerProfileId = models.CharField(max_length=200, null=True)
    locationId = models.CharField(max_length=200, null=True)
    at = models.DateTimeField(auto_now=True, null=True)
    compensation = models.ForeignKey(
        Compensation,
        on_delete=models.SET_NULL,
        related_name='compensation',
        null=True,
        blank=True
    )


class Query(models.Model):
    query_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    # a 'keywords' like this
    # [0]-> [a][b], [1]-> [c] means looks for (a & b) or (c)
    keywords = models.CharField(max_length=1000)  # string [][]
    employer_names = models.CharField(max_length=200)  # string []
    compensation = models.CharField(max_length=200)  # number []
    compensation_unit = models.CharField(max_length=20)
    commute_time = models.IntegerField(max_length=200)  # in minutes, i.e 60 = 60 minutes
    commute_options = models.CharField(max_length=200)  # comma delimited list of option, i.e. transit,driving
    frequency = models.CharField(max_length=20)  # daily, bi-daily, weekly, monthly
    location_ids = models.CharField(max_length=200)  # string []
    updated = models.DateField()
    has_contact = models.BooleanField()


from django.db.models.fields import Field


@Field.register_lookup
class Search(models.Lookup):
    lookup_name = 'search'

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params
