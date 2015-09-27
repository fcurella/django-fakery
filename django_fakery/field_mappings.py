import os

from django import VERSION as django_version
from django.db import models


def comma_sep_integers(faker, field, *args, **kwargs):
    return ','.join([faker.random_int() for _ in range(10)])


def decimal(faker, field, *args, **kwargs):
    right_digits = field.decimal_places
    left_digits = field.max_digits - right_digits
    return faker.pydecimal(left_digits=left_digits, right_digits=right_digits, positive=True)


def random_bytes(faker, field, length, *args, **kwargs):
    return os.urandom(length)


mappings_types = {
    models.BigIntegerField: ('random_int', [], {'min': -9223372036854775808, 'max': 9223372036854775807}),
    models.BinaryField: (random_bytes, [1024], {}),
    models.BooleanField: ('pybool', [], {}),
    models.CharField: ('word', [], {}),
    models.CommaSeparatedIntegerField: (comma_sep_integers, [], {}),
    models.DateField: (lambda faker, field: faker.date_time().date(), [], {}),
    models.DateTimeField: ('date_time', [], {}),
    models.DecimalField: (decimal, [], {}),
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
}

if django_version >= (1, 8, 0):
    mappings_types.update({
        models.DurationField: ('time_delta', [], {}),
        models.UUIDField: ('uuid4', [], {}),
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
