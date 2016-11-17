# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_auto_20160720_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='duration',
            field=models.IntegerField(default=60),
            preserve_default=False,
        ),
    ]
