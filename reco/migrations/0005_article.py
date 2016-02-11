# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reco', '0004_userprofile_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=128)),
                ('content', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('url', models.URLField()),
                ('author', models.ManyToManyField(to='reco.UserProfile')),
            ],
        ),
    ]
