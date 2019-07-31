.. ref-get_or_make

Get or Make
-----------

You can check for existence of a model instance and create it if necessary by using the ``g_m`` (short for ``get_or_make``) method:

.. code-block:: python

    from myapp.models import MyModel

    myinstance, created = factory.g_m(
        MyModel,
        lookup={
            'myfield': 'myvalue',
        }
    )(myotherfield='somevalue')

If you're looking for a more explicit API, you can use the ``.get_or_make()`` method:

.. code-block:: python

    from myapp.models import MyModel

    myinstance, created = factory.get_or_make(
        MyModel,
        lookup={
            'myfield': 'myvalue',
        },
        fields={
            'myotherfield': 'somevalue',
        },
    )
