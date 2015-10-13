import random

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import NOT_PROVIDED

from faker import Factory as FakerFactory

from .compat import get_model_fields, string_types
from .exceptions import ForeignKeyError
from .lazy import Lazy
from .utils import language_to_locale
from .values import Evaluator


user_model = get_user_model()

locale = language_to_locale(settings.LANGUAGE_CODE)


class Factory(object):
    def __init__(self, fake=None):
        self.fake = fake or FakerFactory.create(locale)

    def seed(self, seed, set_global=False):
        self.fake.seed(seed)
        if set_global:
            random.seed(seed)

    def blueprint(self, *args, **kwargs):
        from .blueprint import Blueprint
        return Blueprint(*args, **kwargs)

    def build_one(self, model, fields=None, pre_save=None, seed=None, make_fks=False, iteration=None):
        if fields is None:
            fields = {}

        if pre_save is None:
            pre_save = []

        if seed:
            fake = FakerFactory.create(locale)
            fake.seed(seed)
        else:
            fake = self.fake

        evaluator = Evaluator(fake, factory=self, iteration=iteration)

        if isinstance(model, string_types):
            model = apps.get_model(*model.split('.'))
        instance = model()
        m2ms = {}
        lazies = []

        for field_name, model_field in get_model_fields(model):
            if isinstance(model_field, models.AutoField):
                continue

            if field_name not in fields and (model_field.blank or model_field.null or model_field.default != NOT_PROVIDED):
                continue

            if field_name not in fields and isinstance(model_field, models.ManyToManyField):
                continue

            if isinstance(model_field, models.ForeignKey):
                if not make_fks:
                    raise ForeignKeyError('field %s is a ForeignKey' % field_name)

            if field_name in fields:
                value = evaluator.evaluate(fields[field_name])
            else:
                value = evaluator.fake_value(model, model_field)

            if model_field.choices:
                value = fake.random_element(model_field.choices)[0]

            if isinstance(value, Lazy):
                lazies.append((field_name, value))
                continue

            if isinstance(model_field, models.ForeignKey):
                field_name += '_id'
                value = value.pk

            if isinstance(model_field, models.ManyToManyField):
                m2ms[field_name] = value
            # special case for user passwords
            if model == user_model and field_name == 'password':
                instance.set_password(value)
            else:
                if field_name not in m2ms:
                    setattr(instance, field_name, value)

        for field_name, lazy in lazies:
            value = getattr(instance, lazy.name)
            if callable(value):
                value = value(*lazy.args, **lazy.kwargs)
            setattr(instance, field_name, value)

        for func in pre_save:
            func(instance)

        return instance, m2ms

    def build(self, model, fields=None, pre_save=None, seed=None, quantity=None, make_fks=False):
        if fields is None:
            fields = {}

        if quantity:
            return [self.build_one(model, fields, pre_save, seed, make_fks, i)[0] for i in range(quantity)]
        else:
            return self.build_one(model, fields, pre_save, seed, make_fks)[0]

    def make_one(self, model, fields=None, pre_save=None, post_save=None, seed=None, iteration=None):
        if fields is None:
            fields = {}

        if post_save is None:
            post_save = []

        instance, m2ms = self.build_one(model, fields, pre_save, seed, make_fks=True, iteration=iteration)
        instance.save()

        for field, relateds in m2ms.items():
            setattr(instance, field, relateds)

        for func in post_save:
            func(instance)
        return instance

    def make(self, model, fields=None, pre_save=None, post_save=None, seed=None, quantity=None):
        if fields is None:
            fields = {}
        if quantity:
            return [self.make_one(model, fields, pre_save, post_save, seed, i) for i in range(quantity)]
        else:
            return self.make_one(model, fields, pre_save, post_save, seed)

factory = Factory()
