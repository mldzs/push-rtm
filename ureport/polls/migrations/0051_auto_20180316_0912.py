# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-16 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0050_auto_20170615_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='backend',
            field=models.CharField(default='rapidpro', max_length=16),
        ),
        migrations.AddField(
            model_name='pollresult',
            name='backend',
            field=models.CharField(default='rapidpro', max_length=16),
        ),
    ]
