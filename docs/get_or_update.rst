.. ref-get_or_update

Get or Update
-------------

You can check for existence of a model instance and update it by using the ``g_u`` (short for ``get_or_update``) method:

.. code-block:: python

    myinstance, created = factory.g_u(
        'myapp.Model',
        lookup={
            'myfield': 'myvalue',
        }
    )(myotherfield='somevalue')

If you're looking for a more explicit API, you can use the ``.get_or_update()`` method:

.. code-block:: python

    myinstance, created = factory.get_or_update(
        'myapp.Model',
        lookup={
            'myfield': 'myvalue',
        },
        fields={
            'myotherfield': 'somevalue',
        },
    )
