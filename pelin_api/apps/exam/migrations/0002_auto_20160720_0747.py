# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answerchoice',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='answer_a',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='answer_b',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='answer_c',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='answer_d',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='answer_key',
            field=models.CharField(default='', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='studentanswer',
            name='answer',
            field=models.CharField(max_length=1),
        ),
        migrations.DeleteModel(
            name='AnswerChoice',
        ),
    ]
