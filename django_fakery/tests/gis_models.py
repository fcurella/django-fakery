from django.contrib.gis.db import models


class Pizzeria(models.Model):
    hq = models.PointField()
    directions = models.LineStringField()
    floor_plan = models.PolygonField()
    locations = models.MultiPointField()
    routes = models.MultiLineStringField()
    delivery_areas = models.MultiPolygonField()
    all_the_things = models.GeometryCollectionField()
