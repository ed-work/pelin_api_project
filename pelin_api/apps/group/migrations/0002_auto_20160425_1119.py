# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pendingapproval',
            old_name='student',
            new_name='user',
        ),
    ]
