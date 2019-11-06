# Generated by Django 2.2.5 on 2019-10-17 14:05

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("taggit", "0003_taggeditem_add_unique_index"),
        ("orgs", "0026_fix_org_config_rapidpro"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Flow",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, help_text="Whether this item is active, use this instead of deleting"
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        help_text="When this item was originally created",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        help_text="When this item was last modified",
                    ),
                ),
                ("name", models.CharField(help_text="The name for flow", max_length=128)),
                ("description", models.TextField()),
                ("collected_data", models.TextField(help_text="What data does this data collect from contacts?")),
                (
                    "sdgs",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(
                            choices=[
                                (1, "No Poverty"),
                                (2, "Zero Hunger"),
                                (3, "Good Health and Well-Being"),
                                (4, "Quality Education"),
                                (5, "Gender Equality"),
                                (6, "Clean Water and Sanitation"),
                                (7, "Affordable And Clean Energy"),
                                (8, "Decent Work and Economic Growth"),
                                (9, "Industry, Innovation and Infrastructure"),
                                (10, "Reduced Inequalities"),
                                (11, "Sustainable Cities and Communities"),
                                (12, "Responsible Production and Consumption"),
                                (13, "Climate Action"),
                                (14, "Life Below Water"),
                                (15, "Life On Land"),
                                (16, "Peace, Justice and Strong Institutions"),
                                (17, "Partnerships for the Goals"),
                            ]
                        ),
                        size=None,
                    ),
                ),
                ("flow", django.contrib.postgres.fields.jsonb.JSONField()),
                ("visible_globally", models.BooleanField(default=False)),
                (
                    "languages",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("bs", "Bosnian"),
                                ("en", "English"),
                                ("fr", "French"),
                                ("es", "Spanish"),
                                ("ar", "Arabic"),
                                ("pt", "Portuguese"),
                                ("pt-br", "Brazilian Portuguese"),
                                ("uk", "Ukrainian"),
                                ("uz", "Uzbek"),
                                ("my", "Burmese"),
                                ("id", "Indonesian"),
                                ("it", "Italian"),
                                ("ro", "Romanian"),
                                ("vi", "Vietnamese"),
                                ("sr-latn", "Latin Serbian"),
                            ],
                            max_length=255,
                        ),
                        size=None,
                    ),
                ),
                ("downloads", models.IntegerField(default=0)),
                ("stars", models.IntegerField(default=0)),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="The user which originally created this item",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="flowhub_flow_creations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        help_text="The user which last modified this item",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="flowhub_flow_modifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "org",
                    models.ForeignKey(
                        help_text="The organization this flow is part of",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="flows",
                        to="orgs.Org",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={"verbose_name": "Flow", "verbose_name_plural": "Flows"},
        )
    ]
