.. ref-seeding:

Seeding the faker
-----------------

.. code-block:: python

    from django_fakery import factory

    factory.make('auth.User', fields={
        'username': 'regularuser_{}'
    }, seed=1234, quantity=4)