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

    factory.m('app.Model')(field='value')

Alternatively, you can use a more explict API:

.. code-block:: python

    from django_fakery import factory

    factory.make(
        'app.Model',
        fields={
            'field': 'value',
        }
    )

We will use the short API throught the documentation.

The value of a field can be any python object, a callable, or a lambda:

.. code-block:: python

    from django_fakery import factory
    from django.utils import timezone

    factory.m('app.Model')(created=timezone.now)

When using a lambda, it will receive two arguments: ``n`` is the iteration number, and ``f`` is an instance of ``faker``:

.. code-block:: python

    user = factory.m('auth.User')(
        username=lambda n, f: 'user_{}'.format(n),
    )

``django-fakery`` includes some pre-built lambdas for common needs. See shortcuts_  for more info.


You can create multiple objects by using the ``quantity`` parameter:

.. code-block:: python

    from django_fakery import factory

    factory.m('app.Model', quantity=4)

For convenience, when the value of a field is a string, it will be interpolated with the iteration number:

.. code-block:: python

    user = factory.m('auth.User', quantity=4)(
        username='user_{}',        
    )

Foreign keys
------------

Non-nullable ``ForeignKey`` s create related objects automatically.

If you want to explicitly create a related object, you can pass a factory like any other value:

.. code-block:: python

    pizza = factory.m('food.Pizza')(
        chef=factory.m('auth.User)(username='Gusteau'),
    )

ManyToManies
------------

Because ``ManyToManyField``s are implicitly nullable (ie: they're always allowed to have their ``.count()`` equal to ``0``), related objects on those fields are not automatically created for you.

If you want to explicitly create a related objects, you can pass a list as the field's value:

.. code-block:: python

    pizza = factory.m('food.Pizza')(
        toppings=[
            factory.m('food.Topping')(name='Anchovies')
        ],
    )

You can also pass a factory, to create multiple objects:

.. code-block:: python

    pizza = factory.m('food.Pizza')(
        toppings=factory.m('food.Topping', quantity=5),
    )

.. _shortcuts:

Shortcuts
---------

``django-fakery`` includes some shortcut functions to generate commonly needed values.


``future_datetime(end='+30d')``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a ``datetime`` object in the future (that is, 1 second from now) up to the specified ``end``. ``end`` can be a string, anotther datetime, or a timedelta. If it's a string, it must start with `+`, followed by and integer and a unit, Eg: ``'+30d'``. Defaults to ``'+30d'``

Valid units are:

* ``'years'``, ``'y'``
* ``'weeks'``, ``'w'``
* ``'days'``, ``'d'``
* ``'hours'``, ``'hours'``
* ``'minutes'``, ``'m'``
* ``'seconds'``, ``'s'``

Example::

    from django_fakery import factory, shortcuts
    factory.m('app.Model')(field=shortcuts.future_datetime('+1w'))


``future_date(end='+30d')``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a ``date`` object in the future (that is, 1 day from now) up to the specified ``end``. ``end`` can be a string, another date, or a timedelta. If it's a string, it must start with `+`, followed by and integer and a unit, Eg: ``'+30d'``. Defaults to ``'+30d'``

``past_datetime(start='-30d')``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a ``datetime`` object in the past between 1 second ago and the specified ``start``. ``start`` can be a string, another datetime, or a timedelta. If it's a string, it must start with `-`, followed by and integer and a unit, Eg: ``'-30d'``. Defaults to ``'-30d'``

``past_date(start='-30d')``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a ``date`` object in the past between 1 day ago and the specified ``start``. ``start`` can be a string, another date, or a timedelta. If it's a string, it must start with `-`, followed by and integer and a unit, Eg: ``'-30d'``. Defaults to ``'-30d'``


Lazies
------

You can refer to the created instance's own attributes or method by using `Lazy` objects.

For example, if you'd like to create user with email as username, and have them always match, you could do:

.. code-block:: python

    from django_fakery import factory, Lazy

    factory.m('auth.User')(
        username=Lazy('email'),
    )


If you want to assign a value returned by a method on the instance, you can pass the method's arguments to the ``Lazy`` object:

.. code-block:: python

    from django_fakery import factory, Lazy

    factory.m('myapp.Model')(
        myfield=Lazy('model_method', 'argument', keyword='keyword value'),
    )

Pre-save and Post-save hooks
----------------------------

You can define functions to be called right before the instance is saved or right after:

.. code-block:: python

    from django_fakery import factory

    factory.m(
        'auth.User',
        pre_save=[
            lambda u: u.set_password('password')
        ],
    )(username='username')

Since settings a user's password is such a common case, we special-cased that scenario, so you can just pass it as a field:

.. code-block:: python

    from django_fakery import factory

    factory.m('auth.User')(
        username='username',
        password='password',
    )

Get or Make
-----------

You can check for existance of a model instance and create it if necessary by using the ``g_m`` (short for ``get_or_make``) method:

.. code-block:: python

    myinstance, created = factory.g_m(
        'myapp.Model',
        lookup={
            'myfield': 'myvalue',
        }
    )(myotherfield='somevalue')

If you're looking for a more explicit API, you can use the ``.get_or_make()`` method:

.. code-block:: python

    myinstance, created = factory.get_or_make(
        'myapp.Model',
        lookup={
            'myfield': 'myvalue',
        },
        fields={
            'myotherfield': 'somevalue',
        },
    )

Non persistent instances
------------------------

You can build instances that are not saved to the database by using the ``.b()`` method, just like you'd use ``.m()``:

.. code-block:: python

    from django_fakery import factory

    factory.b('app.Model')(
        field='value',
    )

Note that since the instance is not saved to the database, ``.build()`` does not support ManyToManies or post-save hooks.

If you're looking for a more explicit API, you can use the ``.build()`` method:

.. code-block:: python

    from django_fakery import factory

    factory.build(
        'app.Model',
        fields={
            'field': 'value',
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

    pizza = factory.blueprint('food.Pizza').fields(
            chef=user,
        )
    )

You can also override the field values you previously specified:

.. code-block:: python

    pizza = factory.blueprint('food.Pizza').fields(
            chef=user,
            thickness=1
        )
    )

    pizza.m(quantity=10)(thickness=2)

Or, if you'd rather use the explicit api:

.. code-block:: python

    pizza = factory.blueprint('food.Pizza').fields(
            chef=user,
            thickness=1
        )
    )

    thicker_pizza = pizza.fields(thickness=2)
    thicker_pizza.make(quantity=10)


Seeding the faker
-----------------

.. code-block:: python

    from django_fakery import factory

    factory.m('auth.User', seed=1234, quantity=4)(
        username='regularuser_{}'
    )

Credits
-------

The API is heavily inspired by `model_mommy`_.

.. _model_mommy: https://github.com/vandersonmota/model_mommy

License
-------

This software is released under the MIT License.
