Django-fakery
=============

.. image:: https://badge.fury.io/py/django-fakery.svg
    :target: https://badge.fury.io/py/django-fakery

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
    from myapp.models import MyModel

    factory.m(MyModel)(field='value')

If you're having issues with circular imports, you can also reference a model by using the ``M`` utility function:

.. code-block:: python

    from django_fakery import factory, M

    factory.m(M("myapp.MyModel"))(field="value")


If you really don't want to import things, you could also just reference a model by using the ``<app_label>.<ModelName>`` syntax. This is not encouraged, as it will likely break type-hinting:

.. code-block:: python

    from django_fakery import factory

    factory.m("myapp.MyModel")(field="value")


If you use ``pytest``, you can use the ``fakery`` fixture (requires ``pytest`` and ``pytest-django``):

.. code-block:: python

    import pytest
    from myapp.models import MyModel

    @pytest.mark.django_db
    def test_mymodel(fakery):
        fakery.m(MyModel)(field='value')

If you'd rather, you can use a more wordy API:

.. code-block:: python

    from django_fakery import factory
    from myapp.models import MyModel

    factory.make(
        MyModel,
        fields={
            'field': 'value',
        }
    )

We will use the short API thorough the documentation.

The value of a field can be any python object, a callable, or a lambda:

.. code-block:: python

    from django.utils import timezone
    from django_fakery import factory
    from myapp.models import MyModel

    factory.m(MyModel)(created=timezone.now)

When using a lambda, it will receive two arguments: ``n`` is the iteration number, and ``f`` is an instance of ``faker``:

.. code-block:: python

    from django.contrib.auth.models import User

    user = factory.m(User)(
        username=lambda n, f: 'user_{}'.format(n),
    )

``django-fakery`` includes some pre-built lambdas for common needs. See shortcuts_  for more info.

You can create multiple objects by using the ``quantity`` parameter:

.. code-block:: python

    from django_fakery import factory
    from django.contrib.auth.models import User

    factory.m(User, quantity=4)

For convenience, when the value of a field is a string, it will be interpolated with the iteration number:

.. code-block:: python

    from myapp.models import MyModel

    user = factory.m(User, quantity=4)(
        username='user_{}',        
    )

Custom fields
-------------

You can add support for custom fields by adding your
custom field class and a function in ``factory.field_types``:

.. code-block:: python

  from django_fakery import factory

  from my_fields import CustomField

  def func(faker, field, count, *args, **kwargs):
      return 43


  factory.field_types.add(
      CustomField, (func, [], {})
  )


As a shortcut, you can specified any Faker function by its name:

.. code-block:: python

  from django_fakery import factory

  from my_fields import CustomField


  factory.field_types.add(
      CustomField, ("random_int", [], {"min": 0, "max": 60})
  )

Foreign keys
------------

Non-nullable ``ForeignKey`` s create related objects automatically.

If you want to explicitly create a related object, you can pass a factory like any other value:

.. code-block:: python

    from django.contrib.auth.models import User
    from food.models import Pizza

    pizza = factory.m(Pizza)(
        chef=factory.m(User)(username='Gusteau'),
    )

If you'd rather not create related objects and reuse the same value for a foreign key, you can use the special value ``django_fakery.rels.SELECT``:

.. code-block:: python

    from django_fakery import factory, rels
    from food.models import Pizza

    pizza = factory.m(Pizza, quantity=5)(
        chef=rels.SELECT,
    )

``django-fakery`` will always use the first instance of the related model, creating one if necessary.

ManyToManies
------------

Because ``ManyToManyField`` s are implicitly nullable (ie: they're always allowed to have their ``.count()`` equal to ``0``), related objects on those fields are not automatically created for you.

If you want to explicitly create a related objects, you can pass a list as the field's value:

.. code-block:: python

    from food.models import Pizza, Topping

    pizza = factory.m(Pizza)(
        toppings=[
            factory.m(Topping)(name='Anchovies')
        ],
    )

You can also pass a factory, to create multiple objects:

.. code-block:: python

    from food.models import Pizza, Topping

    pizza = factory.m(Pizza)(
        toppings=factory.m(Topping, quantity=5),
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

Example:

.. code-block:: python

    from django_fakery import factory, shortcuts
    from myapp.models import MyModel

    factory.m(MyModel)(field=shortcuts.future_datetime('+1w'))


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
    from django.contrib.auth.models import User

    factory.m(auth.User)(
        username=Lazy('email'),
    )


If you want to assign a value returned by a method on the instance, you can pass the method's arguments to the ``Lazy`` object:

.. code-block:: python

    from django_fakery import factory, Lazy
    from myapp.models import MyModel

    factory.m(MyModel)(
        myfield=Lazy('model_method', 'argument', keyword='keyword value'),
    )

Pre-save and Post-save hooks
----------------------------

You can define functions to be called right before the instance is saved or right after:

.. code-block:: python

    from django.contrib.auth.models import User
    from django_fakery import factory

    factory.m(
        User,
        pre_save=[
            lambda u: u.set_password('password')
        ],
    )(username='username')

Since settings a user's password is such a common case, we special-cased that scenario, so you can just pass it as a field:

.. code-block:: python

    from django.contrib.auth.models import User
    from django_fakery import factory

    factory.m(User)(
        username='username',
        password='password',
    )

Get or Make
-----------

You can check for existance of a model instance and create it if necessary by using the ``g_m`` (short for ``get_or_make``) method:

.. code-block:: python

    from myapp.models import MyModel

    myinstance, created = factory.g_m(
        MyModel,
        lookup={
            'myfield': 'myvalue',
        }
    )(myotherfield='somevalue')

If you're looking for a more explicit API, you can use the ``.get_or_make()`` method:

.. code-block:: python

    from myapp.models import MyModel

    myinstance, created = factory.get_or_make(
        MyModel,
        lookup={
            'myfield': 'myvalue',
        },
        fields={
            'myotherfield': 'somevalue',
        },
    )

Get or Update
-------------

You can check for existence of a model instance and update it by using the ``g_u`` (short for ``get_or_update``) method:

.. code-block:: python

    from myapp.models import MyModel

    myinstance, created = factory.g_u(
        MyModel,
        lookup={
            'myfield': 'myvalue',
        }
    )(myotherfield='somevalue')

If you're looking for a more explicit API, you can use the ``.get_or_update()`` method:

.. code-block:: python

    from myapp.models import MyModel

    myinstance, created = factory.get_or_update(
        MyModel,
        lookup={
            'myfield': 'myvalue',
        },
        fields={
            'myotherfield': 'somevalue',
        },
    )

Non-persistent instances
------------------------

You can build instances that are not saved to the database by using the ``.b()`` method, just like you'd use ``.m()``:

.. code-block:: python

    from django_fakery import factory
    from myapp.models import MyModel

    factory.b(MyModel)(
        field='value',
    )

Note that since the instance is not saved to the database, ``.build()`` does not support ManyToManies or post-save hooks.

If you're looking for a more explicit API, you can use the ``.build()`` method:

.. code-block:: python

    from django_fakery import factory
    from myapp.models import MyModel

    factory.build(
        MyModel,
        fields={
            'field': 'value',
        }
    )


Blueprints
----------

Use a blueprint:

.. code-block:: python

    from django.contrib.auth.models import User
    from django_fakery import factory

    user = factory.blueprint(User)

    user.make(quantity=10)

Blueprints can refer other blueprints:

.. code-block:: python

    from food.models import Pizza

    pizza = factory.blueprint(Pizza).fields(
            chef=user,
        )
    )

You can also override the field values you previously specified:

.. code-block:: python

    from food.models import Pizza

    pizza = factory.blueprint(Pizza).fields(
            chef=user,
            thickness=1
        )
    )

    pizza.m(quantity=10)(thickness=2)

Or, if you'd rather use the explicit api:

.. code-block:: python

    from food.models import Pizza

    pizza = factory.blueprint(Pizza).fields(
            chef=user,
            thickness=1
        )
    )

    thicker_pizza = pizza.fields(thickness=2)
    thicker_pizza.make(quantity=10)


Seeding the faker
-----------------

.. code-block:: python

    from django.contrib.auth.models import User
    from django_fakery import factory

    factory.m(User, seed=1234, quantity=4)(
        username='regularuser_{}'
    )

Credits
-------

The API is heavily inspired by `model_mommy`_.

.. _model_mommy: https://github.com/vandersonmota/model_mommy

License
-------

This software is released under the MIT License.
