.. ref-hooks:

Pre-save and Post-save hooks
----------------------------

You can define functions to be called right before the instance is saved or right after:

.. code-block:: python

    from django_fakery import factory

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

    from django_fakery import factory

    factory.make(
        'auth.User',
        fields={
            'username': 'username',
            'password': 'password',
        }
    )