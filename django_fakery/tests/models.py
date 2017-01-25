from decimal import Decimal
from django import VERSION as django_version
from django.contrib.gis.geos import HAS_GEOS
from django.contrib.postgres import fields as postgres_fields
from django.db import models

from autoslug import AutoSlugField


class Chef(models.Model):
    slug = AutoSlugField()
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email_address = models.EmailField()
    twitter_profile = models.URLField()


class Topping(models.Model):
    name = models.CharField(max_length=60)


class Pizza(models.Model):
    THICKNESSES = (
        (0, 'thin'),
        (1, 'thick'),
        (2, 'deep dish'),
    )

    name = models.CharField(max_length=50)
    price = models.DecimalField(null=True, decimal_places=2, max_digits=4)
    gluten_free = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    thickness = models.CharField(max_length=50, choices=THICKNESSES)
    backed_on = models.DateTimeField()
    rating = models.PositiveSmallIntegerField()

    chef = models.ForeignKey(Chef, related_name='invented_pizzas')
    critic = models.ForeignKey(Chef, null=True, related_name='reviewed_pizzas')
    toppings = models.ManyToManyField(Topping, related_name='pizzas')
    unique_comment = models.TextField(unique=True)

    def get_price(self, tax):
        return (Decimal('7.99') + (Decimal('7.99') * Decimal(tax))).quantize(Decimal('0.01'))


if HAS_GEOS:
    from django.contrib.gis.db import models as geo_models

if django_version < (1, 9, 0):
    class Pizzeria(geo_models.Model):
        hq = geo_models.PointField()
        directions = geo_models.LineStringField()
        floor_plan = geo_models.PolygonField()
        locations = geo_models.MultiPointField()
        routes = geo_models.MultiLineStringField()
        delivery_areas = geo_models.MultiPolygonField()
        all_the_things = geo_models.GeometryCollectionField()
else:
    class Pizzeria(geo_models.Model):
        hq = geo_models.PointField()
        directions = geo_models.LineStringField()
        floor_plan = geo_models.PolygonField()
        locations = geo_models.MultiPointField()
        routes = geo_models.MultiLineStringField()
        delivery_areas = geo_models.MultiPolygonField()
        all_the_things = geo_models.GeometryCollectionField()
        rast = geo_models.RasterField()


if django_version < (1, 9, 0):
    class SpecialtyPizza(models.Model):
        toppings = postgres_fields.ArrayField(
            models.CharField(max_length=20),
            size=4
        )
        metadata = postgres_fields.HStoreField()
        price_range = postgres_fields.IntegerRangeField()
        sales = postgres_fields.BigIntegerRangeField()
        available_on = postgres_fields.DateTimeRangeField()
        season = postgres_fields.DateRangeField()
else:
    class SpecialtyPizza(models.Model):
        toppings = postgres_fields.ArrayField(
            models.CharField(max_length=20),
            size=4
        )
        metadata = postgres_fields.HStoreField()
        price_range = postgres_fields.IntegerRangeField()
        sales = postgres_fields.BigIntegerRangeField()
        available_on = postgres_fields.DateTimeRangeField()
        season = postgres_fields.DateRangeField()
        nutritional_values = postgres_fields.JSONField()
