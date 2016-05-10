# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 7, 16, 32, 16, 420356), auto_now=True),
            preserve_default=False,
        ),
    ]
