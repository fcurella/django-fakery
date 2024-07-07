import sys

from datetime import datetime
from unittest import skipIf

from django.test import TestCase

from django_fakery import factory
from django_fakery.compat import HAS_PSYCOPG2

if HAS_PSYCOPG2:
    from psycopg2.extras import DateTimeTZRange, NumericRange

PYPY3 = hasattr(sys, "pypy_version_info") and sys.version_info.major >= 3


@skipIf(not HAS_PSYCOPG2, "Psycopg2 not installed")
@skipIf(PYPY3, "Psycopg2cffi does not support Python3")
class PostgresTest(TestCase):
    def test_postgres_fields(self):
        gigis_special = factory.make("tests.SpecialtyPizza")
        self.assertTrue(isinstance(gigis_special.toppings, list))
        for topping in gigis_special.toppings:
            self.assertTrue(isinstance(topping, str))

        self.assertTrue(isinstance(gigis_special.metadata, dict))
        self.assertTrue(isinstance(gigis_special.price_range, NumericRange))
        self.assertTrue(isinstance(gigis_special.price_range.lower, int))
        self.assertTrue(isinstance(gigis_special.sales, NumericRange))
        self.assertTrue(isinstance(gigis_special.sales.lower, int))
        self.assertTrue(isinstance(gigis_special.available_on, DateTimeTZRange))
        self.assertTrue(isinstance(gigis_special.available_on.lower, datetime))
        self.assertNotEqual(gigis_special.available_on.lower.tzinfo, None)
        self.assertTrue(isinstance(gigis_special.nutritional_values, dict))

    def test_json(self):
        gigis_special = factory.make(
            "tests.SpecialtyPizza", fields={"nutritional_values": {"Calories": 310}}
        )
        self.assertEqual(gigis_special.nutritional_values, {"Calories": 310})

        gigis_special, created = factory.update_or_make(
            "tests.SpecialtyPizza",
            lookup={"id": gigis_special.id},
            fields={
                "nutritional_values": {"Calories": {"Total": 310, "From Fat": 120}}
            },
        )
        self.assertFalse(created)
        self.assertEqual(
            gigis_special.nutritional_values,
            {"Calories": {"Total": 310, "From Fat": 120}},
        )

        summer_special, created = factory.update_or_make(
            "tests.SpecialtyPizza",
            lookup={"name": "Summer Special"},
            fields={
                "nutritional_values": {"Calories": {"Total": 310, "From Fat": 120}}
            },
        )

        self.assertTrue(created)
        self.assertEqual(
            summer_special.nutritional_values,
            {"Calories": {"Total": 310, "From Fat": 120}},
        )

    def test_array(self):
        gigis_special = factory.make(
            "tests.SpecialtyPizza",
            fields={"toppings": ["black olives", "green olives"]},
        )
        self.assertEqual(gigis_special.toppings, ["black olives", "green olives"])

        gigis_special, created = factory.update_or_make(
            "tests.SpecialtyPizza",
            lookup={"id": gigis_special.id},
            fields={"toppings": ["black olives", "green olives", "cremini mushrooms"]},
        )
        self.assertFalse(created)
        self.assertEqual(
            gigis_special.toppings,
            ["black olives", "green olives", "cremini mushrooms"],
        )

        summer_special, created = factory.update_or_make(
            "tests.SpecialtyPizza",
            lookup={"name": "Summer Special"},
            fields={"toppings": ["black olives", "green olives", "cremini mushrooms"]},
        )

        self.assertTrue(created)
        self.assertEqual(
            summer_special.toppings,
            ["black olives", "green olives", "cremini mushrooms"],
        )
