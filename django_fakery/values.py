from functools import partial
from django.db import models

from .compat import get_related_model, string_types

from . import field_mappings


class Evaluator(object):
    def __init__(self, faker, factory, iteration):
        self.faker = faker
        self.factory = factory
        self.iteration = iteration
        super(Evaluator, self).__init__()

    def evaluate(self, value):
        from .blueprint import Blueprint

        if isinstance(value, Blueprint):
            return value.make_one(iteration=self.iteration)
        if callable(value):
            if value.__name__ == '<lambda>':
                return value(self.iteration, self.faker)
            else:
                return value()
        if isinstance(value, string_types):
            return value.format(self.iteration, self.faker)
        return value

    def evaluate_fake(self, resolver, field):
        if callable(resolver[0]):
            func = partial(resolver[0], self.faker, field)
        else:
            func = getattr(self.faker, resolver[0])
        return func(*resolver[1], **resolver[2])

    def fake_value(self, field):
        if isinstance(field, models.ForeignKey):
            return self.factory.make_one(get_related_model(field), iteration=self.iteration)

        if field.name in field_mappings.mappings_names:
            return self.evaluate_fake(field_mappings.mappings_names[field.name], field)

        if field.__class__ in field_mappings.mappings_types:
            return self.evaluate_fake(field_mappings.mappings_types[field.__class__], field)

        raise ValueError('Cant generate a value for field `%s`' % field.name)
