VERSION = "3.0.1"

from django.utils.functional import SimpleLazyObject
from django.utils.module_loading import import_string

from .blueprint import Blueprint
from .lazy import Lazy
from .utils import get_model as M

factory = SimpleLazyObject(lambda: import_string("django_fakery.faker_factory.factory"))
