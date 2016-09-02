.. ref-quickstart:

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


You can create multiple objects by using the ``quantity`` parameter:

.. code-block:: python

    from django_fakery import factory

    factory.m('app.Model', quantity=4)

For convenience, when the value of a field is a string, it will be interpolated with the iteration number:

.. code-block:: python

    user = factory.m('auth.User', quantity=4)(
        username='user_{}',        
    )
