# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 21:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jogo',
            old_name='horario',
            new_name='inicio',
        ),
        migrations.AddField(
            model_name='jogo',
            name='termino',
            field=models.TimeField(default=datetime.datetime(2016, 7, 16, 21, 36, 52, 780146, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
