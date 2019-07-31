.. ref-shortcuts:

Shortcuts
---------

``django-fakery`` includes some shortcut functions to generate commonly needed values.


``future_datetime(end='+30d')``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a ``datetime`` object in the future (that is, 1 second from now) up to the specified ``end``. ``end`` can be a string, anotther datetime, or a timedelta. If it's a string, it must start with `+`, followed by and integer and a unit, Eg: ``'+30d'``. Defaults to ``'+30d'``

Valid units are:

* ``'years'``, ``'y'``
* ``'weeks'``, ``'w'``
* ``'days'``, ``'d'``
* ``'hours'``, ``'hours'``
* ``'minutes'``, ``'m'``
* ``'seconds'``, ``'s'``

Example::

    from django_fakery import factory, shortcuts
    from myapp.models import MyModel

    factory.m(MyModel)(field=shortcuts.future_datetime('+1w'))


``future_date(end='+30d')``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a ``date`` object in the future (that is, 1 day from now) up to the specified ``end``. ``end`` can be a string, another date, or a timedelta. If it's a string, it must start with `+`, followed by and integer and a unit, Eg: ``'+30d'``. Defaults to ``'+30d'``

Valid units are:

* ``'years'``, ``'y'``
* ``'weeks'``, ``'w'``
* ``'days'``, ``'d'``
* ``'hours'``, ``'hours'``
* ``'minutes'``, ``'m'``
* ``'seconds'``, ``'s'``

Example::

    from django_fakery import factory, shortcuts
    from myapp.models import MyModel

    factory.m(MyModel)(field=shortcuts.future_date('+1w'))


``past_datetime(start='-30d')``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a ``datetime`` object in the past between 1 second ago and the specified ``start``. ``start`` can be a string, another datetime, or a timedelta. If it's a string, it must start with `-`, followed by and integer and a unit, Eg: ``'-30d'``. Defaults to ``'-30d'``

Valid units are:

* ``'years'``, ``'y'``
* ``'weeks'``, ``'w'``
* ``'days'``, ``'d'``
* ``'hours'``, ``'h'``
* ``'minutes'``, ``'m'``
* ``'seconds'``, ``'s'``

Example::

    from django_fakery import factory, shortcuts
    from myapp.models import MyModel

    factory.m(MyModel)(field=shortcuts.past_datetime('-1w'))


``past_date(start='-30d')``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a ``date`` object in the past between 1 day ago and the specified ``start``. ``start`` can be a string, another date, or a timedelta. If it's a string, it must start with `-`, followed by and integer and a unit, Eg: ``'-30d'``. Defaults to ``'-30d'``

Valid units are:

* ``'years'``, ``'y'``
* ``'weeks'``, ``'w'``
* ``'days'``, ``'d'``
* ``'hours'``, ``'h'``
* ``'minutes'``, ``'m'``
* ``'seconds'``, ``'s'``

Example::

    from django_fakery import factory, shortcuts
    from myapp.models import MyModel

    factory.m(MyModel)(field=shortcuts.past_date('-1w'))
