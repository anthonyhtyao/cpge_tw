# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reco', '0007_auto_20160210_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='url',
        ),
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(default='qq'),
            preserve_default=False,
        ),
    ]
