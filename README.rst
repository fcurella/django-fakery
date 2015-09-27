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

Pre-save and Post-save hooks
----------------------------

You can define functions to be called right before the instance is saved or right after:

.. code-block:: python

    from django_fakery.lazy import Lazy

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

    from django_fakery.lazy import Lazy

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

    from django_fakery.lazy import Lazy

    factory.make(
        'auth.User',
        fields={
            'username': Lazy('email'),
        }
    )


If you want to assign a value returned by a method on the instance, you can pass the method's argument to the ``Lazy`` object:

.. code-block:: python

    from django_fakery.lazy import Lazy

    factory.make(
        'myapp.Model',
        fields={
            'myfield': Lazy('model_method', 'argument', keyword='keyword value'),
        }
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

* callable shortcuts
* contrib fields
* localization
* self-referencing models

License
-------

This software is released under the MIT License.
