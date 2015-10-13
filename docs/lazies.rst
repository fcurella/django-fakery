.. ref-lazies:

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
