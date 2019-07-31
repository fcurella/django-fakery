import pytest

from django_fakery import factory


@pytest.fixture
def fakery():
    return factory
