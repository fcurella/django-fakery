from django.test import TestCase

from django_fakery.utils import language_to_locale


class UtilsTest(TestCase):
    def test_language_to_locale(self):
        locale = language_to_locale('en')
        self.assertEqual(locale, 'en')

        locale = language_to_locale('en-us')
        self.assertEqual(locale, 'en_US')
