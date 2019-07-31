.. ref-hooks:

Pre-save and Post-save hooks
----------------------------

You can define functions to be called right before the instance is saved or right after:

.. code-block:: python

    from django.contrib.auth.models import User
    from django_fakery import factory

    factory.m(
        User,
        pre_save=[
            lambda i: i.set_password('password')
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
