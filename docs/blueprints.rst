.. ref-blueprints:

Blueprints
----------

Use a blueprint:

.. code-block:: python

    from django_fakery import factory

    user = factory.blueprint('auth.User')

    user.make(quantity=10)

Blueprints can refer other blueprints:

.. code-block:: python

    pizza = factory.blueprint(
        'food.Pizza',
        fields={
            'chef': user,
        }
    )
