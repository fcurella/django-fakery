.. ref-relathionships:

Relationship Fields
-------------------

Foreign keys
============

Non-nullable ``ForeignKey`` s create related objects automatically.

If you want to explicitly create a related object, you can pass it like any other value:

.. code-block:: python

    pizza = factory.m('food.Pizza')(
        chef=factory.m('auth.User)(username='Gusteau'),
    )

ManyToManies
============

Because ``ManyToManyField``s are implicitly nullable (ie: they're always allowed to have their ``.count()`` equal to ``0``), related objects on those fields are not automatically created for you.

If you want to explicitly create a related objects, you can pass a list as the field's value:

.. code-block:: python

    pizza = factory.m('food.Pizza')(
        toppings=[
            factory.m('food.Tooping)(name='Anchovies')
        ],
    )

You can also pass a factory, to create multiple objects:

.. code-block:: python

    pizza = factory.m('food.Pizza')(
        toppings=factory.m('food.Tooping', quantity=5),
    )
