.. ref-lazies:

Lazies
------

You can refer to the created instance's own attributes or method by using `Lazy` objects.

For example, if you'd like to create user with email as username, and have them always match, you could do:

.. code-block:: python

    from django_fakery import factory, Lazy

    factory.m('auth.User')(
        username=Lazy('email'),
    )


If you want to assign a value returned by a method on the instance, you can pass the method's arguments to the ``Lazy`` object:

.. code-block:: python

    from django_fakery import factory, Lazy

    factory.make('myapp.Model')
        myfield=Lazy('model_method', 'argument', keyword='keyword value'),
    )
