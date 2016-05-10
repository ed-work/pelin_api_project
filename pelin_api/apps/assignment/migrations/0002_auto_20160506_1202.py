# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.assignment.models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentfiles',
            name='assignment',
        ),
        migrations.AddField(
            model_name='assignment',
            name='file',
            field=models.FileField(default='tes', upload_to=apps.assignment.models.generate_filename),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='AssignmentFiles',
        ),
    ]
