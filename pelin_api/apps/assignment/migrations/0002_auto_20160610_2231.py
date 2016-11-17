# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submittedassignment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignment',
            name='group',
            field=models.ForeignKey(to='group.Group'),
        ),
    ]
