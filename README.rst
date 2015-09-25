Django-fakery
=============

.. image:: https://travis-ci.org/fcurella/django-fakery.svg?branch=master
    :target: https://travis-ci.org/fcurella/django-fakery

An easy-to-use implementation of `Creation Methods`_ for Django, backed by ``Faker``.

.. _Creation Methods: http://xunitpatterns.com/Creation%20Method.html

``django_fakery`` will try to guess the field's value based on the field's name and type.

QuickStart
----------

::

    from django_fakery.factory import factory

    factory.make('auth.User', quantity=4)


Blueprints
----------

::
    from django_fakery.blueprint import Blueprint

    user = Blueprint('auth.User')

    user.make(quantity=10)

If you want to ensure uniqueness when generating multiple objects, you can use a lambda function.

In this example, ``n`` is the iteration number, and ``f`` is an instance of ``faker``::


    user = Blueprint(
        'auth.User',
        fields={
            'username': lambda n, f: 'user_%s' % n,
        }
    )

For convenience, when the value is a string, you can simply pass a formatting string:

::

    user = Blueprint(
        'auth.User',
        fields={
            'username': 'user_%(n)s',
        }
    )

Blueprints can refer other blueprints:

    pizza = Blueprint(
        'food.Pizza',
        fields={
            'chef': user,
        }
    )

Seeding the faker
-----------------

::

    from django_fakery.factory import Factory

    factory = Factory()

    factory.seed(1234)

    factory.make('auth.User', fields={
        'username': 'regularuser'
    }, seed=1234, quantity=4)


::

    from django_fakery.factory import factory

    factory.make('auth.User', fields={
        'username': 'regularuser'
    }, seed=1234, quantity=4)

License
-------

This software is released under the MIT License.
