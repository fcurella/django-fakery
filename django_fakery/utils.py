from typing import overload

from django.apps import apps
from django.db import models

from six import string_types

from .types import T


def language_to_locale(language):
    """
    Converts django's `LANGUAGE_CODE` settings to a proper locale code.
    """
    tokens = language.split("-")
    if len(tokens) == 1:
        return tokens[0]
    return "%s_%s" % (tokens[0], tokens[1].upper())


@overload
def get_model(model):
    # type: (str) -> models.Model
    pass


@overload
def get_model(model):
    # type: (T) -> T
    pass


def get_model(model):
    if isinstance(model, string_types):
        model = apps.get_model(*model.split("."))
    return model


def get_model_fields(model):
    fields = list(model._meta._forward_fields_map.items())
    for m2m in model._meta.many_to_many:
        fields.append((m2m.name, m2m))
    return fields


def set_related(instance, attr, value):
    field = getattr(instance, attr)
    field.set(value)
