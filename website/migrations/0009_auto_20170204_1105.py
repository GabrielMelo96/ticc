# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-04 13:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20170204_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match', to='website.Competition'),
        ),
    ]
