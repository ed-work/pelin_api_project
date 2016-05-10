# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.assignment.models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0002_auto_20160506_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='file',
            field=models.FileField(null=True, upload_to=apps.assignment.models.generate_filename, blank=True),
        ),
    ]
