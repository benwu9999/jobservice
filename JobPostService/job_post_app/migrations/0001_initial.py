# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-25 00:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compensation',
            fields=[
                ('compensationId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0, null=True)),
                ('duration', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'compensation',
            },
        ),
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('jobPostId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('employerProfileId', models.CharField(max_length=200, null=True)),
                ('locationId', models.CharField(max_length=200, null=True)),
                ('at', models.DateTimeField(auto_now=True, null=True)),
                ('compensation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='compensation', to='job_post_app.Compensation')),
            ],
            options={
                'db_table': 'job_post',
            },
        ),
    ]