# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-26 18:49
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    def remove_inactive_boundaries(apps, schema_editor):
        Boundary = apps.get_model('locations', 'Boundary')

        deleted, inactive = Boundary.objects.filter(is_active=False).delete()

        print("Deleted %d inactive boundaries" % deleted)

    dependencies = [
        ('locations', '0002_boundary_is_active'),
    ]

    operations = [
        migrations.RunPython(remove_inactive_boundaries),
    ]
