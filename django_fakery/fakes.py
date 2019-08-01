from django.utils import text, timezone

from faker.generator import random

from .compat import HAS_GEOS, HAS_PSYCOPG2


def comma_sep_integers(faker, field, *args, **kwargs):
    return ",".join([faker.random_int() for _ in range(10)])


def decimal(faker, field, *args, **kwargs):
    right_digits = field.decimal_places
    left_digits = field.max_digits - right_digits
    return faker.pydecimal(
        left_digits=left_digits, right_digits=right_digits, positive=True
    )


def slug(faker, field, count, *args, **kwargs):
    return text.slugify("-".join(faker.words(nb=count)))[: field.max_length]


if HAS_GEOS:
    from django.contrib.gis import gdal, geos

    def point(faker, field, srid):
        lat = random.uniform(-180.0, 180.0)
        lng = random.uniform(-90, 90)

        if field.dim == 2:
            return geos.Point(lat, lng, srid=srid)
        else:
            alt = random.uniform(-4000.0, 9000.0)
            return geos.Point(lat, lng, alt, srid=srid)

    def linestring(faker, field, srid, *args, **kwargs):
        point_count = faker.random_int(min=2, max=10)

        points = [point(faker, field, srid) for _ in range(point_count)]
        return geos.LineString(*points)

    def linearring(faker, field, srid, *args, **kwargs):
        point_0 = point(faker, field, srid)
        point_1 = point(faker, field, srid)
        point_2 = point(faker, field, srid)
        point_3 = geos.Point(point_0.x, point_0.y)
        points = [point_0, point_1, point_2, point_3]
        return geos.LinearRing(*points)

    def polygon(faker, field, srid, *args, **kwargs):
        ring = linearring(faker, field, srid)
        return geos.Polygon(ring)

    def collection(faker, field, srid, element_func, geometry_class, *args, **kwargs):
        element_count = faker.random_int(min=1, max=10)
        elements = [element_func(faker, field, srid) for _ in range(element_count)]

        return geometry_class(*elements)

    def multipoint(faker, field, srid, *args, **kwargs):
        return collection(faker, field, srid, point, geos.MultiPoint)

    def multilinestring(faker, field, srid, *args, **kwargs):
        return collection(faker, field, srid, linestring, geos.MultiLineString)

    def multipolygon(faker, field, srid, *args, **kwargs):
        return collection(faker, field, srid, polygon, geos.MultiPolygon)

    def geometrycollection(faker, field, srid, *args, **kwargs):
        single_point = point(faker, field, srid)
        points = collection(faker, field, srid, point, geos.MultiPoint)
        geometries = [single_point] + points
        return geos.GeometryCollection(*geometries)

    def gdal_raster(faker, field, srid, *args, **kwargs):
        scale = faker.pyfloat(positive=True)
        return gdal.GDALRaster(
            {
                "width": faker.random_int(min=1, max=1024),
                "height": faker.random_int(min=1, max=1024),
                "name": faker.word(),
                "srid": srid,
                "scale": [scale, -scale],
                "bands": [{"data": range(faker.random_int(min=1, max=1024))}],
            }
        )


if HAS_PSYCOPG2:
    from psycopg2.extras import DateRange, DateTimeTZRange, NumericRange

    def array(faker, field, *args, **kwargs):
        from .field_mappings import mappings_types
        from .values import Evaluator

        if field.size:
            size = field.size
        else:
            size = 10
        element_count = faker.random_int(min=1, max=size)

        evaluator = Evaluator(faker=faker, factory=None, iteration=None)

        fake = mappings_types[field.base_field.__class__]
        return [evaluator.evaluate_fake(fake, field) for _ in range(element_count)]

    def integerrange(faker, field, min, max, *args, **kwargs):
        lower = faker.random_int(min=min, max=max - 1)
        upper = faker.random_int(min=lower, max=max)
        return NumericRange(lower, upper)

    def floatrange(faker, field, *args, **kwargs):
        lower = random.uniform(-2147483647, 2147483646)
        upper = random.uniform(lower, 2147483647)
        return NumericRange(lower, upper)

    def datetimerange(faker, field, *args, **kwargs):
        lower = timezone.make_aware(faker.date_time())
        upper = timezone.make_aware(faker.date_time_between_dates(datetime_start=lower))
        return DateTimeTZRange(lower, upper)

    def daterange(faker, field, *args, **kwargs):
        lower = faker.date_time().date()
        upper = faker.date_time_between_dates(datetime_start=lower).date()
        return DateRange(lower, upper)

    def random_dict(faker, field, *args, **kwargs):
        return faker.pydict(10, True, int, str)
