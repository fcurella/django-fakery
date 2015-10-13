.. ref-relathionships:

Relationship Fields
-------------------

Foreign keys
============

Non-nullable ``ForeignKey``s create related objects automatically.

If you want to explicitly create a related object, you can pass it to the ``fields`` like any other value:

.. code-block:: python

    pizza = factory.make(
        'food.Pizza',
        fields={
            'chef': factory.make('auth.User', fields={'username': 'Gusteau'}),
        }
    )

ManyToManies
============

Because ``ManyToManyField``s are implicitly nullable (ie: they're always allowed to have their ``.count()`` equal to ``0``), related objects on those fields are not automatically created for you.

If you want to explicitly create a related objects, you can pass a list to the ``fields`` like any other value:

.. code-block:: python

    pizza = factory.make(
        'food.Pizza',
        fields={
            'toppings': [factory.make('food.Tooping', fields={'name': 'Anchovies'})],
        }
    )

You can also pass a factory, to create multiple objects:

.. code-block:: python

    pizza = factory.make(
        'food.Pizza',
        fields={
            'toppings': factory.make('food.Tooping', quantity=5),
        }
    )
