.. ref-custom_fields

Custom fields
-------------

You can add support for custom fields by adding your
custom field class and a function in ``factory.field_types``:

.. code-block:: python

  from django_fakery import factory

  from my_fields import CustomField

  def func(faker, field, count, *args, **kwargs):
      return 43


  factory.field_types.add(
      CustomField, (func, [], {})
  )


.. code-block:: python


As a shortcut, you can specified any Faker function by its name:

.. code-block:: python

  from django_fakery import factory

  from my_fields import CustomField


  factory.field_types.add(
      CustomField, ("random_int", [], {"min": 0, "max": 60})
  )
