# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-04 13:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20170204_1113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matchscore',
            old_name='game',
            new_name='match',
        ),
    ]
