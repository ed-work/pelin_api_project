# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160610_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reg_id',
            field=models.CharField(max_length=162, null=True, blank=True),
        ),
    ]
