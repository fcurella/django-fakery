.. ref-nonpersistentinstances:

Non persistent instances
------------------------

You can build instances that are not saved to the database by using the `.build()` method, just like you'd use `.make()`:

.. code-block:: python

    from django_fakery import factory

    factory.build(
        'app.Model',
        fields={
            'field': 'value',
        }
    )

Note that since the instance is not saved to the database, `.build()` does not support ManyToManies or post-save hooks.