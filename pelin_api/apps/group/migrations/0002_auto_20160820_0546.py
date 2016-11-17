# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='semester',
            field=models.IntegerField(choices=[(1, b'I'), (2, b'II'), (3, b'III'), (4, b'IV'), (5, b'V'), (6, b'VI'), (7, b'VII'), (8, b'VII')]),
        ),
    ]
