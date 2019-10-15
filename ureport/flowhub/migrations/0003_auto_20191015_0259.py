# Generated by Django 2.2.5 on 2019-10-15 05:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowhub', '0002_auto_20191015_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='languages',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('bs', 'Bosnian'), ('en', 'English'), ('fr', 'French'), ('es', 'Spanish'), ('ar', 'Arabic'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('uk', 'Ukrainian'), ('uz', 'Uzbek'), ('my', 'Burmese'), ('id', 'Indonesian'), ('it', 'Italian'), ('ro', 'Romanian'), ('vi', 'Vietnamese'), ('sr-latn', 'Latin Serbian')], max_length=255), size=None),
        ),
    ]
