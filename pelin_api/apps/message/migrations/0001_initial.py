# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reciever', models.ForeignKey(related_name='conversation_reciever', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='conversation_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b's', max_length=1, choices=[(b's', b'Send'), (b'r', b'Read')])),
                ('conversation', models.ForeignKey(to='message.Conversation')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('visible_to', models.ForeignKey(related_name='message_visible_to', default=None, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
