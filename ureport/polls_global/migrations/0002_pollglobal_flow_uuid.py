# Generated by Django 2.2.5 on 2020-01-13 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_global', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollglobal',
            name='flow_uuid',
            field=models.CharField(default=' ', help_text='The Flow this Poll is based on', max_length=36),
            preserve_default=False,
        ),
    ]
