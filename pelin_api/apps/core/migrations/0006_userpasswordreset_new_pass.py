# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_userpasswordreset'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpasswordreset',
            name='new_pass',
            field=models.CharField(default='random', max_length=12),
            preserve_default=False,
        ),
    ]
