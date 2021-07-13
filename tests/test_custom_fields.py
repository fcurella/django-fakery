from django.test import TestCase
from django_fakery import factory

from .models import Inventory, CustomIntegerField


class CustomFieldsTest(TestCase):
    def test_custom_field(self):
        factory.field_types.add(CustomIntegerField, (lambda faker, field: 3, [], {}))
        inventory = factory.m(Inventory)()
        assert inventory.in_stock == 3
