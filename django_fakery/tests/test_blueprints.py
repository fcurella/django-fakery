from django.test import TestCase

from .blueprints import pizza


class FactoryTest(TestCase):
    def test_blueprint(self):
        movie_night = pizza.make(quantity=10)
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, 'Chef 0')
        self.assertEqual(movie_night[1].chef.first_name, 'Chef 1')

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
