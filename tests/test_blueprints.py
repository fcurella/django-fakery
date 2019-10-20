from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import get_current_timezone

from tests.blueprints import pizza, pizza_short


class BlueprintTest(TestCase):
    def test_blueprint(self):
        movie_night = pizza.make(quantity=10)
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, "Chef 0")
        self.assertEqual(movie_night[1].chef.first_name, "Chef 1")

        now = timezone.now()
        baked_pizza = pizza.make()
        difference = now - baked_pizza.baked_on
        self.assertTrue(difference.total_seconds() <= 3600)

    def test_blueprint_build(self):
        movie_night = pizza.build(quantity=10)
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, "Chef 0")
        self.assertEqual(movie_night[1].chef.first_name, "Chef 1")
        self.assertEqual(movie_night[0].thickness, 1)
        self.assertEqual(movie_night[1].thickness, 1)

        movie_night = pizza.build(quantity=10, make_fks=True)
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, "Chef 0")
        self.assertEqual(movie_night[1].chef.first_name, "Chef 1")
        self.assertEqual(movie_night[0].thickness, 1)
        self.assertEqual(movie_night[1].thickness, 1)

    def test_blueprint_build_override(self):
        movie_night = pizza.build(quantity=10, fields={"thickness": 2})
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].thickness, 2)
        self.assertEqual(movie_night[1].thickness, 2)

    def test_blueprint_fields_returns_copy_with_updated_fields(self):
        thick_pizzas = pizza.fields(thickness=3).build(quantity=3)
        self.assertEqual(thick_pizzas[0].thickness, 3, "thickness should be udpated")
        self.assertEqual(
            thick_pizzas[1].chef.first_name,
            "Chef 1",
            "chef should still be set from the previous blueprint",
        )

    def test_blueprint_fields_make_with_fields(self):
        """check that blueprint.fields(...).make(fields=...) works as expected"""
        p = pizza.fields(thickness=3).make(fields={"thickness": 5})
        self.assertEqual(p.thickness, 5)

    def test_blueprint_fields_make_one_with_fields(self):
        """check that blueprint.fields(...).make_one(fields=...) works as expected"""
        p = pizza.fields(thickness=3).make_one(fields={"thickness": 5})
        self.assertEqual(p.thickness, 5)


class BlueprintShortTest(TestCase):
    def test_blueprint(self):
        movie_night = pizza_short.m(quantity=10)()
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, "Chef 0")
        self.assertEqual(movie_night[1].chef.first_name, "Chef 1")

    def test_blueprint_build(self):
        movie_night = pizza_short.b(quantity=10)()
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, "Chef 0")
        self.assertEqual(movie_night[1].chef.first_name, "Chef 1")
        self.assertEqual(movie_night[0].thickness, 1)
        self.assertEqual(movie_night[1].thickness, 1)

        movie_night = pizza_short.b(quantity=10, make_fks=True)()
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, "Chef 0")
        self.assertEqual(movie_night[1].chef.first_name, "Chef 1")
        self.assertEqual(movie_night[0].thickness, 1)
        self.assertEqual(movie_night[1].thickness, 1)

    def test_blueprint_build_override(self):
        movie_night = pizza.b(quantity=10)(thickness=2)
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].thickness, 2)
        self.assertEqual(movie_night[1].thickness, 2)

        movie_night = pizza_short.b(quantity=10)(thickness=2)
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].thickness, 2)
        self.assertEqual(movie_night[1].thickness, 2)
