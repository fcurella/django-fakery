import pytest

from django_fakery import factory
from django_fakery import shortcuts as _shortcuts


@pytest.fixture
def fakery():
    return factory


@pytest.fixture
def fakery_shortcuts():
    return _shortcuts
