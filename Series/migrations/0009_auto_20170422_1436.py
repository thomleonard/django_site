# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-22 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Series', '0008_auto_20170422_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvshow',
            name='is_next_episode_available',
            field=models.BooleanField(default=False),
        ),
    ]
