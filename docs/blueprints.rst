.. ref-blueprints:

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
