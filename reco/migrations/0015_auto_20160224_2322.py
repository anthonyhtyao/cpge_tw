# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reco', '0014_auto_20160224_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='grandsecole',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='highschool',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ispublic',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='prepa',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
