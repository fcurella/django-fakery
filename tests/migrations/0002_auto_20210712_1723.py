# Generated by Django 2.2.24 on 2021-07-12 22:23

import django.db.models.deletion

from django.db import migrations, models

import tests.models


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Inventory",
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
                ("in_stock", tests.models.CustomIntegerField()),
                (
                    "pizza",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tests.Pizza"
                    ),
                ),
            ],
        ),
    ]
