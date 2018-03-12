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


If you'd rather not create related objects and reuse the same value for a foreign key, you can use the special value ``django_fakery.rels.SELECT``:

.. code-block:: python

    from django_fakery import factory, rels


    pizza = factory.m('food.Pizza', quantity=5)(
        chef=rels.SELECT,
    )

``django-fakery`` will always use the first instance of the related model, creating one if necessary.


ManyToManies
============

Because ``ManyToManyField`` s are implicitly nullable (ie: they're always allowed to have their ``.count()`` equal to ``0``), related objects on those fields are not automatically created for you.

If you want to explicitly create a related objects, you can pass a list as the field's value:

.. code-block:: python

    pizza = factory.m('food.Pizza')(
        toppings=[
            factory.m('food.Topping')(name='Anchovies')
        ],
    )

You can also pass a factory, to create multiple objects:

.. code-block:: python

    pizza = factory.m('food.Pizza')(
        toppings=factory.m('food.Topping', quantity=5),
    )
