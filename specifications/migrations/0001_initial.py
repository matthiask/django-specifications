# Generated by Django 2.1.1 on 2018-09-29 07:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Specification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
            ],
            options={
                "verbose_name": "specification",
                "verbose_name_plural": "specifications",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="SpecificationField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("text", "text"),
                            ("longtext", "long text"),
                            ("boolean", "boolean"),
                            ("integer", "integer"),
                            ("closed_set_single", "closed set"),
                            ("closed_set_multiple", "closed set (multiple)"),
                            ("open_set_single", "open set"),
                            ("open_set_single_extensible", "open set (extensible)"),
                        ],
                        max_length=30,
                        verbose_name="type",
                    ),
                ),
                (
                    "choices",
                    models.TextField(
                        blank=True,
                        help_text="One choice per line (if applicable).",
                        verbose_name="choices",
                    ),
                ),
                (
                    "help_text",
                    models.CharField(
                        blank=True, default="", max_length=100, verbose_name="help text"
                    ),
                ),
                (
                    "required",
                    models.BooleanField(verbose_name="required", default=True),
                ),
                ("ordering", models.IntegerField(default=0, verbose_name="ordering")),
            ],
            options={
                "verbose_name": "specification field",
                "verbose_name_plural": "specification fields",
                "ordering": ["group__ordering", "ordering"],
            },
        ),
        migrations.CreateModel(
            name="SpecificationFieldGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("ordering", models.IntegerField(default=0, verbose_name="ordering")),
                (
                    "specification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="groups",
                        to="specifications.Specification",
                        verbose_name="specification",
                    ),
                ),
            ],
            options={
                "verbose_name": "specification field group",
                "verbose_name_plural": "specification field groups",
                "ordering": ["ordering"],
            },
        ),
        migrations.AddField(
            model_name="specificationfield",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="fields",
                to="specifications.SpecificationFieldGroup",
                verbose_name="group",
            ),
        ),
        migrations.AddField(
            model_name="specificationfield",
            name="specification",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fields",
                to="specifications.Specification",
                verbose_name="specification",
            ),
        ),
    ]
