from datetime import datetime,  timedelta
from django.utils.timezone import make_aware
from django.test import TestCase

from .blueprints import pizza, pizza_short


class BlueprintTest(TestCase):

    def test_blueprint(self):
        movie_night = pizza.make(quantity=10)
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, 'Chef 0')
        self.assertEqual(movie_night[1].chef.first_name, 'Chef 1')

        now = make_aware(datetime.now())
        baked_pizza = pizza.make()
        difference = now - baked_pizza.baked_on
        self.assertTrue(difference.total_seconds() < 3600)

    def test_blueprint_build(self):
        movie_night = pizza.build(quantity=10)
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, 'Chef 0')
        self.assertEqual(movie_night[1].chef.first_name, 'Chef 1')
        self.assertEqual(movie_night[0].thickness, 1)
        self.assertEqual(movie_night[1].thickness, 1)

        movie_night = pizza.build(quantity=10, make_fks=True)
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, 'Chef 0')
        self.assertEqual(movie_night[1].chef.first_name, 'Chef 1')
        self.assertEqual(movie_night[0].thickness, 1)
        self.assertEqual(movie_night[1].thickness, 1)

    def test_blueprint_build_override(self):
        movie_night = pizza.build(quantity=10, fields={'thickness': 2})
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].thickness, 2)
        self.assertEqual(movie_night[1].thickness, 2)


class BlueprintShortTest(TestCase):
    def test_blueprint(self):
        movie_night = pizza_short.m(quantity=10)()
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, 'Chef 0')
        self.assertEqual(movie_night[1].chef.first_name, 'Chef 1')

    def test_blueprint_build(self):
        movie_night = pizza_short.b(quantity=10)()
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, 'Chef 0')
        self.assertEqual(movie_night[1].chef.first_name, 'Chef 1')
        self.assertEqual(movie_night[0].thickness, 1)
        self.assertEqual(movie_night[1].thickness, 1)

        movie_night = pizza_short.b(quantity=10, make_fks=True)()
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, 'Chef 0')
        self.assertEqual(movie_night[1].chef.first_name, 'Chef 1')
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
