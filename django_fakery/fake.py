from functools import partial
from django.utils.functional import SimpleLazyObject


class LazyFake(SimpleLazyObject):
    def __init__(self, fake, method, *args, **kwargs):
        func = getattr(fake, method)
        return super(LazyFake, self).__init__(partial(func, *args, **kwargs))
