# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_auto_20170319_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compensation',
            name='bitemporal',
        ),
        migrations.AddField(
            model_name='bitemporal',
            name='amount',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='bitemporal',
            name='duration',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Compensation',
        ),
    ]
