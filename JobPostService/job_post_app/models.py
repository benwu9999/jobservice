from __future__ import unicode_literals

import datetime
from django.db import models
import dateutil.parser
import uuid

# fields in model will use camel case so django can parse json which is also camel case

# Create your models here.
from django_unixdatetimefield import UnixDateTimeField


class Compensation(models.Model):
    """
    data model for compensation information
    """

    class Meta:
        db_table = 'compensation'
        # unique_together = ("amount", "duration")

    compensation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.IntegerField(default=0, null=True)
    duration = models.CharField(max_length=200, null=True)
    created = UnixDateTimeField()

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.created = dateutil.parser.parse(self.created)
        super(Compensation, self).save()


class JobPostFullTextSearchQuerySet(models.query.QuerySet):
    # def __init__(self, model=None, fields=None):
    #     super(JobPostFullTextSearchQuerySet, self).__init__(model)
    #
    # def search(self, search_param):
    #     match_expr = ("WHERE MATCH (title,description) AGAINST ('%s' IN BOOLEAN MODE)")
    #
    #     # Add the extra SELECT and WHERE options
    #     return self.extra(where=[match_expr], params=[search_param])
    def __init__(self, model=None, query=None, using=None, hints=None, fields=None):
        super(JobPostFullTextSearchQuerySet, self).__init__(model, query, using, hints)
        self._search_fields = fields

    def search(self, query):
        # Add the extra SELECT and WHERE options
        return self.extra(where=['MATCH(title,description) AGAINST (%s IN BOOLEAN MODE)'], params=[query])


class JobPostFulLTextSearchManager(models.Manager):
    def __init__(self, fields):
        super(JobPostFulLTextSearchManager, self).__init__()
        self._search_fields = fields

    def get_queryset(self):
        return JobPostFullTextSearchQuerySet(model=JobPost, fields=self._search_fields)

    def search(self, query):
        return self.get_queryset().search(query)


class JobPost(models.Model):
    """
    data model for Job Post
    """

    class Meta:
        db_table = 'job_post'

    job_post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    employer_profile_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    location_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    applicable = models.BooleanField(default=False)
    compensation = models.ForeignKey(
        Compensation,
        on_delete=models.SET_NULL,
        related_name='job_posts',
        null=True,
        blank=True,
        db_column='compensation_id'
    )
    created = UnixDateTimeField()
    modified = UnixDateTimeField(auto_now=True)
    hide_contact = models.BooleanField(default=True)
    hide_location = models.BooleanField(default=True)

    objects = models.Manager()
    full_text_search_objects = JobPostFulLTextSearchManager(('title', 'description'))

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.created = dateutil.parser.parse(self.created)
        super(JobPost, self).save()

    def __str__(self):
        return "%s %s" % (self.__class__.__name__, self.job_post_id)


# class Query(models.Model):
#     query_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user_id = models.CharField(max_length=200)
#     name = models.CharField(max_length=200)
#     # a 'keywords' like this
#     # [0]-> [a][b], [1]-> [c] means looks for (a & b) or (c)
#     keywords = models.CharField(max_length=1000)  # string [][]
#     employer_names = models.CharField(max_length=200)  # string []
#     compensation = models.CharField(max_length=200)  # number []
#     compensation_unit = models.CharField(max_length=20)
#     commute_time = models.IntegerField()  # in minutes, i.e 60 = 60 minutes
#     commute_options = models.CharField(max_length=200)  # comma delimited list of option, i.e. transit,driving
#     frequency = models.CharField(max_length=20)  # daily, bi-daily, weekly, monthly
#     location_ids = models.CharField(max_length=200)  # string []
#     has_contact = models.BooleanField()
#     created = UnixDateTimeField()
#     modified = UnixDateTimeField(auto_now=True)
#
#     def save(self, *args, **kwargs):
#         if not self.created:
#             self.created = datetime.datetime.now()
#         else:
#             self.created = dateutil.parser.parse(self.created)
#         super(Query, self).save()

from django.db.models.fields import Field


@Field.register_lookup
class Search(models.Lookup):
    lookup_name = 'search'

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params
