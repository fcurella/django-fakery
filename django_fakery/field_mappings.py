from .compat import django_version, HAS_PSYCOPG2
from django.contrib.gis.db import models as geo_models
from django.db import models

from . import fakes


mappings_types = {
    models.BigIntegerField: ('random_int', [], {'min': -9223372036854775808, 'max': 9223372036854775807}),
    models.BinaryField: (fakes.random_bytes, [1024], {}),
    models.BooleanField: ('pybool', [], {}),
    models.CharField: ('word', [], {}),
    models.CommaSeparatedIntegerField: (fakes.comma_sep_integers, [], {}),
    models.DateField: (lambda faker, field: faker.date_time().date(), [], {}),
    models.DateTimeField: ('date_time', [], {}),
    models.DecimalField: (fakes.decimal, [], {}),
    models.EmailField: ('email', [], {}),
    models.FileField: ('file_name', [], {}),
    models.FilePathField: ('file_name', [], {}),
    models.FloatField: ('pyfloat', [], {}),
    models.ImageField: ('file_name', [], {'extension': 'jpg'}),
    models.IntegerField: ('pyint', [], {}),
    models.IPAddressField: ('ipv4', [], {}),
    models.GenericIPAddressField: ('ipv4', [], {}),
    models.PositiveIntegerField: ('pyint', [], {'max': 2147483647}),
    models.PositiveSmallIntegerField: ('pyint', [], {'max': 32767}),
    models.SlugField: ('word', [], {}),
    models.SmallIntegerField: ('pyint', [], {'min': -32768, 'max': 32767}),
    models.TextField: ('paragraph', [], {}),
    models.TimeField: (lambda faker, field: faker.date_time().time(), [], {}),
    models.URLField: ('url', [], {}),

    geo_models.PointField: (fakes.point, (), {'srid': 4326}),
    geo_models.LineStringField: (fakes.linestring, (), {'srid': 4326}),
    geo_models.PolygonField: (fakes.polygon, (), {'srid': 4326}),
    geo_models.MultiPointField: (fakes.multipoint, (), {'srid': 4326}),
    geo_models.MultiLineStringField: (fakes.multilinestring, (), {'srid': 4326}),
    geo_models.MultiPolygonField: (fakes.multipolygon, (), {'srid': 4326}),
    geo_models.GeometryCollectionField: (fakes.geometrycollection, (), {'srid': 4326}),
}

if django_version >= (1, 8, 0):

    mappings_types.update({
        models.DurationField: ('time_delta', [], {}),
        models.UUIDField: ('uuid4', [], {}),
    })
    if HAS_PSYCOPG2:
        from django.contrib.postgres import fields as pg_fields

        mappings_types.update({
            pg_fields.ArrayField: (fakes.array, [], {}),
            pg_fields.HStoreField: ('pydict', [10, True, 'str'], {}),
            pg_fields.IntegerRangeField: (fakes.integerrange, [], {'min': -2147483647, 'max': 2147483647}),
            pg_fields.BigIntegerRangeField: (fakes.integerrange, [], {'min': -9223372036854775808, 'max': 9223372036854775807}),
            pg_fields.FloatRangeField: (fakes.floatrange, [], {}),
            pg_fields.DateTimeRangeField: (fakes.datetimerange, [], {}),
            pg_fields.DateRangeField: (fakes.daterange, [], {}),
        })

mappings_names = {
    'name': ('word', [], {}),  # `name` is too generic to assume it's a person
    'first_name': ('first_name', [], {}),
    'last_name': ('last_name', [], {}),
    'full_name': ('full_name', [], {}),
    'email': ('email', [], {}),
    'created': ('date_time_between', [], {'start_date': '-30d', 'end_date': '30d'}),
    'created_at': ('date_time_between', [], {'start_date': '-30d', 'end_date': '30d'}),
    'updated': ('date_time_between', [], {'start_date': '-30d', 'end_date': '30d'}),
    'updated_at': ('date_time_between', [], {'start_date': '-30d', 'end_date': '30d'}),
}
