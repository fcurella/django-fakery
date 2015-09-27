from django.test import TestCase

from .blueprints import pizza


class BlueprintTest(TestCase):
    def test_blueprint(self):
        movie_night = pizza.make(quantity=10)
        self.assertEqual(len(movie_night), 10)
        self.assertEqual(movie_night[0].chef.first_name, 'Chef 0')
        self.assertEqual(movie_night[1].chef.first_name, 'Chef 1')
