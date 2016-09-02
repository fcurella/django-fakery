from functools import partial
import random

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import NOT_PROVIDED

from faker import Factory as FakerFactory

from .compat import string_types
from .exceptions import ForeignKeyError
from .lazy import Lazy
from .utils import get_model_fields, language_to_locale
from .values import Evaluator


user_model = get_user_model()

locale = language_to_locale(settings.LANGUAGE_CODE)


class Empty(object):
    pass


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
                _field_name = field_name.split('_id')[0]
                value = fields.get(_field_name, Empty)

                if not make_fks and ((value == Empty) or (value and value.pk is None)):
                    raise ForeignKeyError(
                        "Field {} is a required ForeignKey, but the related {}.{} model"
                        " doesn't have the necessary primary key.".format(
                            field_name,
                            model_field.related_model._meta.app_label,
                            model_field.related_model._meta.model_name,
                        )
                    )

            if field_name in fields:
                value = evaluator.evaluate(fields[field_name])
            else:
                if model_field.choices:
                    value = fake.random_element(model_field.choices)[0]
                else:
                    value = evaluator.fake_value(model, model_field)

            if isinstance(value, Lazy):
                lazies.append((field_name, value))
                continue

            if isinstance(model_field, models.ForeignKey):
                field_name += '_id'
                value = value.pk if value else None

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

    def m(self, model, pre_save=None, post_save=None, seed=None, quantity=None):
        make = partial(self.make, model=model, pre_save=pre_save, post_save=post_save, seed=seed, quantity=quantity)

        def fn(**kwargs):
            return make(fields=kwargs)

        return fn

    def b(self, model, pre_save=None, seed=None, quantity=None, make_fks=False):
        build = partial(self.build, model=model, pre_save=pre_save, seed=seed, quantity=quantity, make_fks=make_fks)

        def fn(**kwargs):
            return build(fields=kwargs)

        return fn

factory = Factory()
