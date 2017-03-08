.. ref-get_or_make

Get or Make
-----------

You can check for existance of a model instance and create it if necessary by using the ``g_m`` (short for ``get_or_make``) method:

.. code-block:: python

    myinstance, created = factory.g_m(
        'myapp.Model',
        lookup={
            'myfield': 'myvalue',
        }
    )(myotherfield='somevalue')

If you're looking for a more explicit API, you can use the ``.get_or_make()`` method:

.. code-block:: python

    myinstance, created = factory.get_or_make(
        'myapp.Model',
        lookup={
            'myfield': 'myvalue',
        },
        fields={
            'myotherfield': 'somevalue',
        },
    )
