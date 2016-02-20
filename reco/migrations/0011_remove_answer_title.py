# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reco', '0010_auto_20160220_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='title',
        ),
    ]
