import sys

from django import VERSION as django_version

try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    psycopg2 = None
    HAS_PSYCOPG2 = False


if sys.version < '3':
    text_type = unicode
    binary_type = str
    string_types = basestring
else:
    text_type = str
    binary_type = bytes
    string_types = str


def get_model_fields(model):
    if django_version < (1, 8, 0):
        fields = [(f.name, f) for f in model._meta.concrete_fields]
    else:
        fields = list(model._meta._forward_fields_map.items())
    for m2m in model._meta.many_to_many:
        fields.append((m2m.name, m2m))
    return fields


def get_related_model(field):
    if django_version < (1, 8, 0):
        return field.related.parent_model
    return field.related_model
