from decimal import Decimal

from django.utils import timezone
from django.test import TestCase

from django_fakery import factory, Lazy
from django_fakery.exceptions import ForeignKeyError


class FactoryTest(TestCase):
    def test_model(self):
        margherita = factory.make('tests.Pizza')

        # field.default
        self.assertFalse(margherita.gluten_free)
        # field.null
        self.assertFalse(margherita.price)

        # field.blank
        self.assertEqual(margherita.description, '')

        # field.choices
        self.assertIn(margherita.thickness, [0, 1, 2])

        # required field
        self.assertNotEqual(margherita.name, '')

        self.assertNotEqual(margherita.chef.first_name, '')

    def test_fields(self):
        margherita = factory.make(
            'tests.Pizza',
            fields={'name': 'four cheeses'}
        )
        self.assertEqual(margherita.name, 'four cheeses')
        self.assertEqual(margherita.description, '')

    def test_blank(self):
        margherita = factory.make(
            'tests.Pizza',
            fields={'name': 'four cheeses', 'description': lambda n, f: f.sentence()}
        )
        self.assertEqual(margherita.name, 'four cheeses')
        self.assertNotEqual(margherita.description, '')

    def test_sequence(self):
        margheritas = factory.make(
            'tests.Pizza',
            fields={'name': 'pizza {}'},
            quantity=10
        )
        self.assertEqual(len(margheritas), 10)
        self.assertEqual(margheritas[0].name, 'pizza 0')
        self.assertEqual(margheritas[1].name, 'pizza 1')

    def test_sequence_callable_lambda(self):
        margheritas = factory.make(
            'tests.Pizza',
            fields={'name': lambda n, f: 'pizza {}'.format(n)},
            quantity=10
        )
        self.assertEqual(len(margheritas), 10)
        self.assertEqual(margheritas[0].name, 'pizza 0')
        self.assertEqual(margheritas[1].name, 'pizza 1')

    def test_sequence_callable(self):
        margheritas = factory.make(
            'tests.Pizza',
            fields={'backed_on': timezone.now},
            quantity=10
        )
        self.assertEqual(len(margheritas), 10)
        self.assertNotEqual(margheritas[0].backed_on, None)
        self.assertNotEqual(margheritas[0].backed_on, margheritas[1].backed_on)

    def test_lazy_field(self):
        chef_masters = factory.make(
            'tests.Chef',
            fields={
                'first_name': 'Chef {}',
                'last_name': Lazy('first_name')
            },
            quantity=10
        )
        self.assertEqual(len(chef_masters), 10)
        self.assertEqual(chef_masters[0].first_name, 'Chef 0')
        self.assertEqual(chef_masters[0].first_name, chef_masters[0].last_name)
        self.assertEqual(chef_masters[1].first_name, 'Chef 1')
        self.assertEqual(chef_masters[0].first_name, chef_masters[0].last_name)

        margherita = factory.make(
            'tests.pizza',
            fields={
                'price': Lazy('get_price', tax=0.07)
            }
        )
        self.assertEqual(margherita.price, Decimal('8.55'))

    def test_foreign_keys(self):
        chef_gusteau = factory.make(
            'tests.Chef',
            fields={
                'first_name': 'Gusteau'
            }
        )

        pizza = factory.make(
            'tests.Pizza',
            fields={
                'chef': chef_gusteau
            }
        )
        self.assertEqual(pizza.chef, chef_gusteau)

    def test_foreign_keys_fail(self):
        chef_gusteau = factory.make(
            'tests.Chef',
            fields={
                'first_name': 'Gusteau'
            }
        )

        self.assertRaises(ForeignKeyError, factory.build,
            'tests.Pizza',
        )
        factory.build(
            'tests.Pizza',
            fields={
                'chef': chef_gusteau,
            }
        )

        chef_skinner = factory.build(
            'tests.Chef',
            fields={
                'first_name': 'Skinner',
            }
        )
        self.assertRaises(ForeignKeyError, factory.build,
            'tests.Pizza',
            fields={
                'chef': chef_skinner,
            }
        )

        factory.build(
            'tests.Pizza',
            fields={
                'chef': chef_gusteau,
                'critic': None,
            }
        )

    def test_manytomany(self):
        pizza = factory.make(
            'tests.Pizza',
        )
        self.assertEqual(pizza.toppings.count(), 0)

        pizza = factory.make(
            'tests.Pizza',
            fields={
                'toppings': [factory.make('tests.Topping')]
            }
        )
        self.assertEqual(pizza.toppings.count(), 1)

        pizza = factory.make(
            'tests.Pizza',
            fields={
                'toppings': factory.make('tests.Topping', quantity=5)
            }
        )
        self.assertEqual(pizza.toppings.count(), 5)

    def test_save_hooks(self):
        user = factory.make(
            'auth.User',
            fields={
                'username': 'username',
            },
            pre_save=[
                lambda i: i.set_password('password')
            ]
        )
        self.assertTrue(user.check_password('password'))

    def test_password(self):
        user = factory.make(
            'auth.User',
            fields={
                'username': 'username',
                'password': 'password'
            }
        )
        self.assertTrue(user.check_password('password'))

    def test_build(self):
        chef_masters = factory.build(
            'tests.Chef',
            fields={
                'first_name': 'Chef {}',
                'last_name': Lazy('first_name')
            },
            quantity=10
        )
        for chef in chef_masters:
            self.assertEqual(chef.id, None)

    def test_field_inheritance(self):
        chef_gusteau = factory.make(
            'tests.Chef',
            fields={
                'first_name': 'Gusteau'
            }
        )
        self.assertTrue('@' in chef_gusteau.email_address)
        self.assertTrue('http://' in chef_gusteau.twitter_profile)
