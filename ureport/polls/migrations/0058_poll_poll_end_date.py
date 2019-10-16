# Generated by Django 2.2.5 on 2019-10-16 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0057_pollquestion_sdgs'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='poll_end_date',
            field=models.DateTimeField(help_text='The date to display for this poll. Leave empty to use flow creation date.', null=True),
        ),
    ]
