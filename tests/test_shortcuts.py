from django.utils import timezone
from django.test import TestCase

from django_fakery import shortcuts

from faker import Faker

fake = Faker()


class ShortcutsTest(TestCase):

    def test_future_datetime(self):
        fn = shortcuts.future_datetime()
        date = fn(1, fake)
        self.assertTrue(date > timezone.now())

        fn = shortcuts.future_datetime('+2d')
        date = fn(1, fake)
        self.assertTrue(date > timezone.now())

    def test_future_date(self):
        fn = shortcuts.future_date()
        date = fn(1, fake)
        self.assertTrue(date > timezone.now().date())

        fn = shortcuts.future_date('+2d')
        date = fn(1, fake)
        self.assertTrue(date > timezone.now().date())

    def test_past_datetime(self):
        fn = shortcuts.past_datetime()
        date = fn(1, fake)
        self.assertTrue(date < timezone.now())

        fn = shortcuts.past_datetime('-2d')
        date = fn(1, fake)
        self.assertTrue(date < timezone.now())

    def test_past_date(self):
        fn = shortcuts.past_date()
        date = fn(1, fake)
        self.assertTrue(date < timezone.now().date())

        fn = shortcuts.past_date('-2d')
        date = fn(1, fake)
        self.assertTrue(date < timezone.now().date())
