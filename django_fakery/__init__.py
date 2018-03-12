VERSION = '1.10.0'

from django.utils.functional import SimpleLazyObject
from django.utils.module_loading import import_string
from .blueprint import Blueprint
from .lazy import Lazy

factory = SimpleLazyObject(lambda: import_string('django_fakery.faker_factory.factory'))
