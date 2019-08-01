.. ref-quickstart:

Installation
------------

Install with::

    $ pip install django-fakery

QuickStart
----------

.. code-block:: python

    from django_fakery import factory
    from myapp.models import MyModel

    factory.m('app.Model')(field='value')

If you're having issues with circular imports, you can also reference a model by using the ``M`` utility function:

.. code-block:: python

    from django_fakery import factory, M

    factory.m(M("myapp.MyModel"))(field="value")


If you really don't like to have to import things, you could also just reference a model by using the ``<app_label>.<ModelName>`` syntax. This is not encouraged, as it will likely break type-hinting:

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
        'app.Model',
        fields={
            'field': 'value',
        }
    )

We will use the short API throught the documentation.

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


``django-fakery`` includes some pre-built lambdas for common needs. See :doc:`shortcuts` for more info.

You can create multiple objects by using the ``quantity`` parameter:

.. code-block:: python

    from django_fakery import factory
    from myapp.models import MyModel

    factory.m(MyModel, quantity=4)

For convenience, when the value of a field is a string, it will be interpolated with the iteration number:

.. code-block:: python

    from django.contrib.auth.models import User

    user = factory.m(User, quantity=4)(
        username='user_{}',        
    )
