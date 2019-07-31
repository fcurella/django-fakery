.. ref-nonpersistantinstances:

Non-persistant Instances
------------------------

You can build instances that are not saved to the database by using the ``.b()`` method, just like you'd use ``.m()``:

.. code-block:: python

    from django_fakery import factory
    from myapp.models import MyModel

    factory.b(MyModel)(
        field='value',
    )

Note that since the instance is not saved to the database, ``.build()`` does not support ManyToManies or post-save hooks.

If you're looking for a more explicit API, you can use the ``.build()`` method:

.. code-block:: python

    from django_fakery import factory
    from myapp.models import MyModel

    factory.build(
        MyModel,
        fields={
            'field': 'value',
        }
    )
