from django import VERSION as django_version
from decimal import Decimal
from django.contrib.gis.db import models


class Chef(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)


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

    chef = models.ForeignKey(Chef)

    def get_price(self, tax):
        return (Decimal('7.99') + (Decimal('7.99') * Decimal(tax))).quantize(Decimal('0.01'))


class Pizzeria(models.Model):
    hq = models.PointField()
    directions = models.LineStringField()
    floor_plan = models.PolygonField()
    locations = models.MultiPointField()
    routes = models.MultiLineStringField()
    delivery_areas = models.MultiPolygonField()
    all_the_things = models.GeometryCollectionField()


if django_version >= (1, 8, 0):
    from django.contrib.postgres import fields as postgres_fields

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
