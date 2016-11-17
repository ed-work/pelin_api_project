# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_userpasswordreset_new_pass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpasswordreset',
            name='code',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='userpasswordreset',
            name='new_pass',
            field=models.CharField(max_length=15),
        ),
    ]
