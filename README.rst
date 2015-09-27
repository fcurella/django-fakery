Django-fakery
=============

.. image:: https://travis-ci.org/fcurella/django-fakery.svg?branch=master
    :target: https://travis-ci.org/fcurella/django-fakery


.. image:: https://coveralls.io/repos/fcurella/django-fakery/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/fcurella/django-fakery?branch=master

An easy-to-use implementation of `Creation Methods`_ for Django, backed by ``Faker``.

.. _Creation Methods: http://xunitpatterns.com/Creation%20Method.html

``django_fakery`` will try to guess the field's value based on the field's name and type.

QuickStart
----------

.. code-block:: python

    from django_fakery.factory import factory

    factory.make('auth.User', quantity=4)

Lazies
------

You can refer to the created instance's own field by using `Lazy` objects.

For example, if you'd like to create user with email as username, and have them always match, you could do:

.. code-block:: python

    from django_fakery.lazy import Lazy

    factory.make(
        'auth.User',
        username=Lazy('email')
    )



Blueprints
----------

.. code-block:: python

    from django_fakery.blueprint import Blueprint

    user = Blueprint('auth.User')

    user.make(quantity=10)

If you want to ensure uniqueness when generating multiple objects, you can use a lambda function.

In this example, ``n`` is the iteration number, and ``f`` is an instance of ``faker``:

.. code-block:: python

    user = Blueprint(
        'auth.User',
        fields={
            'username': lambda n, f: 'user_%s' % n,
        }
    )

For convenience, when the value is a string, you can simply pass a formatting string:

.. code-block:: python

    user = Blueprint(
        'auth.User',
        fields={
            'username': 'user_%(n)s',
        }
    )

Blueprints can refer other blueprints:

.. code-block:: python

    pizza = Blueprint(
        'food.Pizza',
        fields={
            'chef': user,
        }
    )

Seeding the faker
-----------------

.. code-block:: python

    from django_fakery.factory import Factory

    factory = Factory()

    factory.seed(1234)

    factory.make('auth.User', fields={
        'username': 'regularuser'
    }, seed=1234, quantity=4)


.. code-block:: python

    from django_fakery.factory import factory

    factory.make('auth.User', fields={
        'username': 'regularuser'
    }, seed=1234, quantity=4)

TODO
----

* lazy methods
* post-creation hooks
* callable shortcuts in bluprints
* contrib fields
* localization
* self-referencing models

License
-------

This software is released under the MIT License.
