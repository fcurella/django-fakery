# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore

from django.contrib.postgres.operations import CreateExtension, HStoreExtension
from django.db import migrations, models

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

try:
    from django.contrib.gis.geos.libgeos import geos_version_tuple

    HAS_GEOS = geos_version_tuple() >= (3, 3, 0)
except (ImportError, OSError):
    HAS_GEOS = False

if HAS_GEOS:
    import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):
    dependencies = []

    operations = [HStoreExtension()]
    operations += [
        migrations.CreateModel(
            name="Chef",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("slug", models.SlugField()),
                ("first_name", models.CharField(max_length=60)),
                ("last_name", models.CharField(max_length=60)),
                ("uuid_id", models.UUIDField()),
                ("email_address", models.EmailField(max_length=60)),
                ("twitter_profile", models.URLField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name="Topping",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name="Pizza",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "price",
                    models.DecimalField(null=True, max_digits=4, decimal_places=2),
                ),
                ("gluten_free", models.BooleanField(default=False)),
                ("vegan", models.BooleanField()),
                ("description", models.TextField(blank=True)),
                (
                    "thickness",
                    models.CharField(
                        max_length=50,
                        choices=[(0, b"thin"), (1, b"thick"), (2, b"deep dish")],
                    ),
                ),
                ("baked_on", models.DateTimeField()),
                ("expiration", models.DateField()),
                (
                    "chef",
                    models.ForeignKey(
                        to="tests.Chef",
                        on_delete=models.CASCADE,
                        related_name="invented_pizzas",
                    ),
                ),
                (
                    "critic",
                    models.ForeignKey(
                        to="tests.Chef",
                        null=True,
                        on_delete=models.CASCADE,
                        related_name="reviewed_pizzas",
                    ),
                ),
                ("toppings", models.ManyToManyField(to="tests.Topping")),
                ("rating", models.PositiveSmallIntegerField()),
                ("unique_comment", models.TextField()),
            ],
        ),
    ]

    if HAS_GEOS:
        operations += [CreateExtension("postgis_raster")]

        pizzeria_fields = [
            (
                "id",
                models.AutoField(
                    verbose_name="ID",
                    serialize=False,
                    auto_created=True,
                    primary_key=True,
                ),
            ),
            ("hq", django.contrib.gis.db.models.fields.PointField(srid=4326)),
            (
                "directions",
                django.contrib.gis.db.models.fields.LineStringField(srid=4326),
            ),
            ("floor_plan", django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            (
                "locations",
                django.contrib.gis.db.models.fields.MultiPointField(srid=4326),
            ),
            (
                "routes",
                django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326),
            ),
            (
                "delivery_areas",
                django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
            ),
            (
                "all_the_things",
                django.contrib.gis.db.models.fields.GeometryCollectionField(srid=4326),
            ),
            ("rast", django.contrib.gis.db.models.fields.RasterField(srid=4326)),
        ]
        operations += [migrations.CreateModel(name="Pizzeria", fields=pizzeria_fields)]

    specialtypizza_fields = [
        (
            "id",
            models.AutoField(
                verbose_name="ID", serialize=False, auto_created=True, primary_key=True
            ),
        ),
        ("name", models.CharField(max_length=50)),
        (
            "toppings",
            django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=20), size=4
            ),
        ),
        ("metadata", django.contrib.postgres.fields.hstore.HStoreField()),
        ("price_range", django.contrib.postgres.fields.IntegerRangeField()),
        ("sales", django.contrib.postgres.fields.BigIntegerRangeField()),
        ("available_on", django.contrib.postgres.fields.DateTimeRangeField()),
        ("season", django.contrib.postgres.fields.DateRangeField()),
        ("nutritional_values", JSONField()),
    ]

    operations += [
        migrations.CreateModel(name="SpecialtyPizza", fields=specialtypizza_fields)
    ]
