import sys

from django import VERSION as django_version


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
        return [(f.name, f) for f in model._meta.concrete_fields]
    return model._meta._forward_fields_map.items()


def get_related_model(field):
    if django_version < (1, 8, 0):
        return field.related.parent_model
    return field.related_model
