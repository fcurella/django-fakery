from functools import partial
import random

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.forms.models import model_to_dict

from faker import Factory as FakerFactory
from six import string_types

from .exceptions import ForeignKeyError
from .lazy import Lazy
from .utils import get_model_fields, language_to_locale, set_related
from .values import Evaluator
from . import rels


user_model = get_user_model()

locale = language_to_locale(settings.LANGUAGE_CODE)


class Empty(object):
    pass


fks_cache = {}


class Factory(object):

    def __init__(self, fake=None):
        self.fake = fake or FakerFactory.create(locale)

    def _get_model(self, model):
        if isinstance(model, string_types):
            model = apps.get_model(*model.split('.'))
        return model

    def _serialize_instance(self, instance):
        model_fields = dict(get_model_fields(instance))
        attrs = {}
        for k, v in model_to_dict(instance).items():
            if k == instance._meta.pk.name:
                continue

            if isinstance(v, (list, models.QuerySet)):
                continue

            if isinstance(model_fields[k], models.ForeignKey) and not isinstance(v, models.Model):
                attrs[k + '_id'] = v
                continue

            attrs[k] = v

        return attrs

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

        model = self._get_model(model)
        instance = model()
        m2ms = {}
        lazies = []

        model_fields = get_model_fields(model)
        for _field_name, model_field in model_fields:
            value = Empty
            field_name = _field_name

            if _field_name.endswith('_id') and model_field.is_relation:
                continue

            if isinstance(model_field, models.AutoField):
                continue

            if isinstance(model_field, (GenericForeignKey, GenericRelation)):
                continue

            if field_name not in fields and (model_field.null or model_field.default != NOT_PROVIDED):
                continue

            if field_name not in fields and isinstance(model_field, models.ManyToManyField):
                continue

            value = fields.get(field_name, Empty)
            if isinstance(model_field, models.ForeignKey):
                if value == Empty:
                    value = fields.get(field_name + '_id', Empty)

                if value == rels.SELECT:
                    model = model_field.related_model
                    qs = model.objects.all()
                    cache_key = model

                    value = fks_cache.get(cache_key, Empty)

                    if value == Empty:
                        try:
                            value = qs[0]
                        except IndexError:
                            value = evaluator.fake_value(model, model_field)

                        fks_cache[cache_key] = value

                if not make_fks and ((value == Empty) or (value and value.pk is None)):
                    raise ForeignKeyError(
                        "Field {} is a required ForeignKey, but the related {}.{} model"
                        " doesn't have the necessary primary key.".format(
                            field_name,
                            model_field.related_model._meta.app_label,
                            model_field.related_model._meta.model_name,
                        )
                    )

                field_name += '_id'

            if value != Empty:
                value = evaluator.evaluate(value)
            else:
                if model_field.choices:
                    value = fake.random_element(model_field.choices)[0]
                else:
                    value = evaluator.fake_value(model, model_field)

            if isinstance(value, Lazy):
                lazies.append((field_name, value))
                continue

            if isinstance(model_field, models.ForeignKey):
                value = value.pk if hasattr(value, 'pk') else value

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

        # Sometimes the model's field for the primary key as a default, which
        # means ``instance.pk`` is already set. We pass ``force_insert`` as a
        # way to tell downstream code that this is a new model.
        instance.save(force_insert=True)

        for field, relateds in m2ms.items():
            set_related(instance, field, relateds)

        for func in post_save:
            func(instance)
        return instance

    def get_or_make(self, model, lookup=None, fields=None, pre_save=None, post_save=None, seed=None):
        if lookup is None:
            lookup = {}
        if fields is None:
            fields = {}
        if post_save is None:
            post_save = []

        instance, m2ms = self.build_one(model, fields, pre_save, seed, make_fks=True)

        attrs = self._serialize_instance(instance)
        for k in lookup:
            attrs.pop(k, None)
        instance, created = self._get_model(model).objects.get_or_create(defaults=attrs, **lookup)

        for field, relateds in m2ms.items():
            set_related(instance, field, relateds)

        for func in post_save:
            func(instance)
        return instance, created

    def g_m(self, model, lookup=None, pre_save=None, post_save=None, seed=None):
        build = partial(
            self.get_or_make, model=model, lookup=lookup, pre_save=pre_save, post_save=post_save, seed=seed
        )

        def fn(**kwargs):
            return build(fields=kwargs)

        return fn

    def update_or_make(self, model, lookup=None, fields=None, pre_save=None, post_save=None, seed=None):
        if lookup is None:
            lookup = {}
        if fields is None:
            fields = {}
        if post_save is None:
            post_save = []

        model_class = self._get_model(model)

        try:
            instance = model_class.objects.get(**lookup)
        except model_class.DoesNotExist:
            created = True
            params = {k: v for k, v in lookup.items() if '__' not in k}
            params.update(fields)
            instance = self.make(model, params, pre_save, post_save, seed)
        else:
            created = False
            for k, v in fields.items():
                # special case for user passwords
                if model_class == user_model and k == 'password':
                    instance.set_password(v)
                else:
                    setattr(instance, k, v)
            instance.save()

            for func in post_save:
                func(instance)

        return instance, created

    def u_m(self, model, lookup=None, pre_save=None, post_save=None, seed=None):
        build = partial(
            self.update_or_make, model=model, lookup=lookup, pre_save=pre_save, post_save=post_save, seed=seed
        )

        def fn(**kwargs):
            return build(fields=kwargs)

        return fn

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
