# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-05 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Series', '0013_auto_20170405_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvshow',
            name='active_season',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
