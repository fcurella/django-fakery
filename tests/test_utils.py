from django.test import TestCase

from django_fakery.utils import get_model, language_to_locale
from tests.models import Chef


class UtilsTest(TestCase):
    def test_language_to_locale(self):
        locale = language_to_locale("en")
        self.assertEqual(locale, "en")

        locale = language_to_locale("en-us")
        self.assertEqual(locale, "en_US")

    def test_model(self):
        Model = get_model(Chef)
        self.assertEqual(Chef, Model)

        Model = get_model("tests.Chef")
        self.assertEqual(Chef, Model)
