.. ref-seeding:

Seeding the faker
-----------------

.. code-block:: python

    from django_fakery import factory

    factory.m('auth.User', seed=1234, quantity=4)(
        username='regularuser_{}'
    )
