# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import VERSION as django_version

from django.db import models, migrations
import django.contrib.gis.db.models.fields
if django_version >= (1, 8, 0):
    from django.contrib.postgres.operations import HStoreExtension
    import django.contrib.postgres.fields
    import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = []
    if django_version >= (1, 8, 0):
        operations.append(HStoreExtension())

    operations += [
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('gluten_free', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('thickness', models.CharField(max_length=50, choices=[(0, b'thin'), (1, b'thick'), (2, b'deep dish')])),
                ('backed_on', models.DateTimeField()),
                ('chef', models.ForeignKey(to='tests.Chef')),
            ],
        ),
        migrations.CreateModel(
            name='Pizzeria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hq', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('directions', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
                ('floor_plan', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('locations', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
                ('routes', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
                ('delivery_areas', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('all_the_things', django.contrib.gis.db.models.fields.GeometryCollectionField(srid=4326)),
            ],
        )
    ]

    if django_version >= (1, 8, 0):
        operations += [
            migrations.CreateModel(
                name='SpecialtyPizza',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('toppings', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=4)),
                    ('metadata', django.contrib.postgres.fields.hstore.HStoreField()),
                    ('price_range', django.contrib.postgres.fields.IntegerRangeField()),
                    ('sales', django.contrib.postgres.fields.BigIntegerRangeField()),
                    ('available_on', django.contrib.postgres.fields.DateTimeRangeField()),
                    ('season', django.contrib.postgres.fields.DateRangeField()),
                ],
            ),
        ]
