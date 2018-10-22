from decimal import Decimal

from django.utils import timezone
from django.test import TestCase

from django_fakery import factory, Lazy, rels
from django_fakery.exceptions import ForeignKeyError

from tests.models import Chef, Pizza


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

    def test_short_api_m(self):
        margherita = factory.m('tests.Pizza')(name='four cheeses')
        self.assertEqual(margherita.name, 'four cheeses')

        pizzas = factory.m('tests.Pizza', quantity=2)(name='pizza {}')
        self.assertEqual(len(pizzas), 2)
        self.assertEqual(pizzas[0].name, 'pizza 0')
        self.assertEqual(pizzas[1].name, 'pizza 1')

    def test_short_api_b(self):
        gusteau = factory.b('tests.Chef')(first_name='Gusteau')
        self.assertEqual(gusteau.first_name, 'Gusteau')

        chefs = factory.b('tests.Chef', quantity=2)(first_name='Chef {}')
        self.assertEqual(len(chefs), 2)
        self.assertEqual(chefs[0].first_name, 'Chef 0')
        self.assertEqual(chefs[1].first_name, 'Chef 1')

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
            fields={'baked_on': timezone.now},
            quantity=10
        )
        self.assertEqual(len(margheritas), 10)
        self.assertNotEqual(margheritas[0].baked_on, None)
        self.assertNotEqual(margheritas[0].baked_on, margheritas[1].baked_on)

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

        self.assertEqual(Chef.objects.count(), 1)

        pizza = factory.make(
            'tests.Pizza',
            fields={
                'chef': chef_gusteau
            }
        )
        self.assertEqual(pizza.chef, chef_gusteau)
        self.assertEqual(Chef.objects.count(), 1)

    def test_foreign_keys_explicit(self):
        chef_gusteau = factory.make(
            'tests.Chef',
            fields={
                'first_name': 'Gusteau'
            }
        )

        self.assertEqual(Chef.objects.count(), 1)

        pizza = factory.make(
            'tests.Pizza',
            fields={
                'chef_id': chef_gusteau.pk
            }
        )
        self.assertEqual(pizza.chef, chef_gusteau)
        self.assertEqual(Chef.objects.count(), 1)

    def test_foreign_keys_fail(self):
        chef_gusteau = factory.make(
            'tests.Chef',
            fields={
                'last_name': 'Gusteau'
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
                'last_name': 'Skinner',
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

        user, created = factory.update_or_make(
            'auth.User',
            lookup={
                'username': 'username',
            },
            fields={
                'password': 'new_password',
            }
        )
        self.assertFalse(created)
        self.assertTrue(user.check_password('new_password'))

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
                'last_name': 'Gusteau'
            }
        )
        self.assertTrue('@' in chef_gusteau.email_address)
        self.assertTrue(
            chef_gusteau.twitter_profile.startswith('http://') or 
            chef_gusteau.twitter_profile.startswith('https://') 
        )

    def test_get_or_make(self):
        already_there = factory.make(
            'tests.Chef',
            fields={
                'first_name': 'Auguste',
                'last_name': 'Gusteau',
            }
        )

        self.assertEqual(Chef.objects.count(), 1)
        chef_gusteau, created = factory.get_or_make(
            'tests.Chef',
            lookup={
                'last_name': 'Gusteau'
            },
            fields={
                'first_name': 'Remi',
            }
        )
        self.assertEqual(Chef.objects.count(), 1)
        self.assertEqual(already_there, chef_gusteau)
        self.assertFalse(created)

        chef_linguini, created = factory.get_or_make(
            'tests.Chef',
            lookup={
                'last_name': 'Linguini'
            },
            fields={
                'first_name': 'Alfredo',
            }
        )

        self.assertEqual(Chef.objects.count(), 2)
        self.assertTrue(created)
        self.assertEqual(chef_linguini.first_name, 'Alfredo')
        self.assertEqual(chef_linguini.last_name, 'Linguini')

    def test_g_m(self):
        already_there = factory.make(
            'tests.Chef',
            fields={
                'first_name': 'Auguste',
                'last_name': 'Gusteau',
            }
        )

        self.assertEqual(Chef.objects.count(), 1)
        chef_gusteau, created = factory.g_m(
            'tests.Chef',
            lookup={
                'last_name': 'Gusteau'
            },
        )(first_name='Remi')
        self.assertEqual(Chef.objects.count(), 1)
        self.assertEqual(already_there, chef_gusteau)
        self.assertFalse(created)

        chef_linguini, created = factory.g_m(
            'tests.Chef',
            lookup={
                'last_name': 'Linguini'
            },
        )(first_name='Alfredo')

        self.assertEqual(Chef.objects.count(), 2)
        self.assertTrue(created)
        self.assertEqual(chef_linguini.first_name, 'Alfredo')
        self.assertEqual(chef_linguini.last_name, 'Linguini')

    def test_update_or_make(self):
        already_there = factory.make(
            'tests.Chef',
            fields={
                'first_name': 'Auguste',
                'last_name': 'Gusteau',
            }
        )

        self.assertEqual(Chef.objects.count(), 1)
        chef_gusteau, created = factory.update_or_make(
            'tests.Chef',
            lookup={
                'last_name': 'Gusteau'
            },
            fields={
                'first_name': 'Remi',
            }
        )
        self.assertEqual(Chef.objects.count(), 1)
        self.assertEqual(already_there, chef_gusteau)
        self.assertEqual(chef_gusteau.first_name, 'Remi')

        self.assertFalse(created)

        chef_linguini, created = factory.update_or_make(
            'tests.Chef',
            lookup={
                'last_name': 'Linguini'
            },
            fields={
                'first_name': 'Alfredo',
            }
        )

        self.assertEqual(Chef.objects.count(), 2)
        self.assertTrue(created)
        self.assertEqual(chef_linguini.first_name, 'Alfredo')
        self.assertEqual(chef_linguini.last_name, 'Linguini')

    def test_u_m(self):
        already_there = factory.make(
            'tests.Chef',
            fields={
                'first_name': 'Auguste',
                'last_name': 'Gusteau',
            }
        )

        self.assertEqual(Chef.objects.count(), 1)
        chef_gusteau, created = factory.u_m(
            'tests.Chef',
            lookup={
                'last_name': 'Gusteau'
            },
        )(first_name='Remi')
        self.assertEqual(Chef.objects.count(), 1)
        self.assertEqual(already_there, chef_gusteau)
        self.assertEqual(chef_gusteau.first_name, 'Remi')

        self.assertFalse(created)

        chef_linguini, created = factory.u_m(
            'tests.Chef',
            lookup={
                'last_name': 'Linguini'
            },
        )(first_name='Alfredo')

        self.assertEqual(Chef.objects.count(), 2)
        self.assertTrue(created)
        self.assertEqual(chef_linguini.first_name, 'Alfredo')
        self.assertEqual(chef_linguini.last_name, 'Linguini')

    def test_rel(self):
        pizzas = factory.make(
            'tests.Pizza',
             quantity=5,
             fields={
                 'chef': rels.SELECT,
             },
        )
        self.assertEqual(Pizza.objects.count(), 5)
        self.assertEqual(Chef.objects.count(), 1)

        self.assertEqual(pizzas[0].chef, pizzas[1].chef)

    def test_format(self):
        chef = factory.make(Chef, fields={
            'last_name': '{Linguini}'
        })

        self.assertEqual(chef.last_name, '{Linguini}')
