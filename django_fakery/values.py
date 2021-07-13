from functools import partial

from django.db import models

from six import string_types

from . import field_mappings


class Evaluator(object):
    def __init__(
        self,
        faker,
        factory,
        iteration,
        mappings_types=field_mappings.mappings_types,
        mappings_names=field_mappings.mappings_names,
    ):
        self.faker = faker
        self.factory = factory
        self.iteration = iteration
        self.mappings_types = mappings_types
        self.mappings_names = mappings_names
        super(Evaluator, self).__init__()

    def evaluate(self, value):
        from .blueprint import Blueprint

        if isinstance(value, Blueprint):
            return value.make_one(iteration=self.iteration)
        if callable(value):
            if value.__name__ == "<lambda>":
                return value(self.iteration, self.faker)
            else:
                return value()
        if isinstance(value, string_types):
            try:
                return value.format(self.iteration, self.faker)
            except KeyError:
                return value
        return value

    def evaluate_fake(self, resolver, field):
        if callable(resolver[0]):
            func = partial(resolver[0], self.faker, field)
        else:
            func = getattr(self.faker, resolver[0])
        return func(*resolver[1], **resolver[2])

    def fake_value(self, model, field):

        if field.blank and isinstance(field, field_mappings.STRING_FIELDS):
            return ""

        if isinstance(field, models.ForeignKey):
            return self.factory.make_one(field.related_model, iteration=self.iteration)

        if field.name in self.mappings_names:
            return self.evaluate_fake(self.mappings_names[field.name], field)

        for field_class, fake in self.mappings_types.items():
            if isinstance(field, field_class):
                return self.evaluate_fake(fake, field)

        model_name = "%s.%s" % (model._meta.app_label, model._meta.model_name)
        raise ValueError(
            "Cant generate a value for model `%s` field `%s`" % (model_name, field.name)
        )
