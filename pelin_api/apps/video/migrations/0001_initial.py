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
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to=b'')),
                ('category', models.CharField(max_length=50, choices=[(b'Umum', b'Umum'), (b'RPL', b'RPL'), (b'Multimedia', b'Multimedia'), (b'Jaringan', b'Jaringan')])),
                ('user', models.ForeignKey(related_name='uploaded_videos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
