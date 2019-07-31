.. ref-seeding:

Seeding the faker
-----------------

.. code-block:: python

    from django.contrib.auth.models import User
    from django_fakery import factory

    factory.m(User, seed=1234, quantity=4)(
        username='regularuser_{}'
    )
