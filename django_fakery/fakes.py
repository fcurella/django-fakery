import os

from django.contrib.gis import geos
from faker.generator import random


def comma_sep_integers(faker, field, *args, **kwargs):
    return ','.join([faker.random_int() for _ in range(10)])


def decimal(faker, field, *args, **kwargs):
    right_digits = field.decimal_places
    left_digits = field.max_digits - right_digits
    return faker.pydecimal(left_digits=left_digits, right_digits=right_digits, positive=True)


def random_bytes(faker, field, length, *args, **kwargs):
    return os.urandom(length)


def point(faker, field, srid):
    lat = random.uniform(-180.0, 180.0)
    lng = random.uniform(-90, 90)

    if field.dim == 2:
        return geos.Point(lat, lng, srid=srid)
    else:
        alt = random.uniform(-4000.0, 9000.0)
        return geos.Point(lat, lng, alt, srid=srid)


def linestring(faker, field, srid):
    point_count = faker.random_int(min=2, max=10)

    points = [point(faker, field, srid) for _ in range(point_count)]
    return geos.LineString(*points)


def linearring(faker, field, srid):
    point_0 = point(faker, field, srid)
    point_1 = point(faker, field, srid)
    point_2 = point(faker, field, srid)
    point_3 = geos.Point(point_0.x, point_0.y)
    points = [point_0, point_1, point_2, point_3]
    return geos.LinearRing(*points)


def polygon(faker, field, srid):
    ring = linearring(faker, field, srid)
    return geos.Polygon(ring)


def collection(faker, field, srid, element_func, geometry_class):
    element_count = faker.random_int(min=1, max=10)
    elements = [element_func(faker, field, srid) for _ in range(element_count)]

    return geometry_class(*elements)


def multipoint(faker, field, srid):
    return collection(faker, field, srid, point, geos.MultiPoint)


def multilinestring(faker, field, srid):
    return collection(faker, field, srid, linestring, geos.MultiLineString)


def multipolygon(faker, field, srid):
    return collection(faker, field, srid, polygon, geos.MultiPolygon)


def geometrycollection(faker, field, srid):
    single_point = point(faker, field, srid)
    points = collection(faker, field, srid, point, geos.MultiPoint)
    geometries = [single_point] + points
    return geos.GeometryCollection(*geometries)
