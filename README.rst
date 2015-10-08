Django-fakery
=============

.. image:: https://travis-ci.org/fcurella/django-fakery.svg?branch=master
    :target: https://travis-ci.org/fcurella/django-fakery


.. image:: https://coveralls.io/repos/fcurella/django-fakery/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/fcurella/django-fakery?branch=master

An easy-to-use implementation of `Creation Methods`_ (aka Object Factory) for Django, backed by ``Faker``.

.. _Creation Methods: http://xunitpatterns.com/Creation%20Method.html

``django_fakery`` will try to guess the field's value based on the field's name and type.

Installation
------------

Install with::

    $ pip install django-fakery

QuickStart
----------

.. code-block:: python

    from django_fakery import factory

    factory.make(
        'app.Model',
        fields={
            'field': 'value',
        }
    )

The value of a field can be any python object, a callable, or a lambda:

.. code-block:: python

    from django_fakery import factory
    from django.utils import timezone

    factory.make(
        'app.Model',
        fields={
            'created': timezone.now
        }
    )

When using a lambda, it will receive two arguments: ``n`` is the iteration number, and ``f`` is an instance of ``faker``:

.. code-block:: python

    user = factory.make(
        'auth.User',
        fields={
            'username': lambda n, f: 'user_{}'.format(n),
        }
    )


You can create multiple objects by using the ``quantity`` parameter:

.. code-block:: python

    from django_fakery import factory

    factory.make('app.Model', quantity=4)

For convenience, when the value of a field is a string, it will be interpolated with the iteration number:

.. code-block:: python

    user = factory.make(
        'auth.User',
        fields={
            'username': 'user_{}',
        },
        quantity=4
    )

Pre-save and Post-save hooks
----------------------------

You can define functions to be called right before the instance is saved or right after:

.. code-block:: python

    from django_fakery import factory

    factory.make(
        'auth.User',
        fields={
            'username': 'username',
        },
        pre_save=[
            lambda i: i.set_password('password')
        ]
    )



Since settings a user's password is such a common case, we special-cased that scenario, so you can just pass it as a field:

.. code-block:: python

    from django_fakery import factory

    factory.make(
        'auth.User',
        fields={
            'username': 'username',
            'password': 'password',
        }
    )

Lazies
------

You can refer to the created instance's own attributes or method by using `Lazy` objects.

For example, if you'd like to create user with email as username, and have them always match, you could do:

.. code-block:: python

    from django_fakery import factory, Lazy

    factory.make(
        'auth.User',
        fields={
            'username': Lazy('email'),
        }
    )


If you want to assign a value returned by a method on the instance, you can pass the method's arguments to the ``Lazy`` object:

.. code-block:: python

    from django_fakery import factory, Lazy

    factory.make(
        'myapp.Model',
        fields={
            'myfield': Lazy('model_method', 'argument', keyword='keyword value'),
        }
    )


Blueprints
----------

Use a blueprint:

.. code-block:: python

    from django_fakery import factory

    user = factory.blueprint('auth.User')

    user.make(quantity=10)

Blueprints can refer other blueprints:

.. code-block:: python

    pizza = factory.blueprint(
        'food.Pizza',
        fields={
            'chef': user,
        }
    )

Seeding the faker
-----------------

.. code-block:: python

    from django_fakery import factory

    factory.make('auth.User', fields={
        'username': 'regularuser_{}'
    }, seed=1234, quantity=4)


Credits
-------

The API is heavily inspired by `model_mommy`_.

.. _model_mommy: https://github.com/vandersonmota/model_mommy

License
-------

This software is released under the MIT License.
