# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_auto_20160425_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='major',
            field=models.CharField(default='S1 TI', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='semester',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]
