# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-22 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Series', '0016_magnet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magnet',
            name='link',
            field=models.CharField(default=b'', max_length=1000, unique=True),
        ),
    ]
