.. django-fakery documentation master file, created by
   sphinx-quickstart on Tue Oct 13 12:43:11 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-fakery's documentation!
=========================================

An easy-to-use implementation of `Creation Methods`_ (aka Object Factory) for Django, backed by ``Faker``.

.. _Creation Methods: http://xunitpatterns.com/Creation%20Method.html

``django_fakery`` will try to guess the field's value based on the field's name and type.

Installation
------------

Install with::

    $ pip install django-fakery

QuickStart
----------

.. code-block:: python

    from django_fakery import factory
    from myapp.models import MyModel

    factory.make(
        MyModel,
        fields={
            'field': 'value',
        }
    )

Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   shortcuts
   lazies
   custom_fields
   relationships
   hooks
   get_or_make
   get_or_update
   nonpersistantinstances
   blueprints
   seeding



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

