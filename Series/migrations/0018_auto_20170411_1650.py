# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-11 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Series', '0017_auto_20170422_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='available',
        ),
        migrations.AddField(
            model_name='episode',
            name='magnet_update',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
