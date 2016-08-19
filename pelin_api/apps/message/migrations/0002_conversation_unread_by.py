# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='unread_by',
            field=models.ForeignKey(related_name='conversation_unread_by', default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
