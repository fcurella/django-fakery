from typing import Any

from .compat import NoReturn


class Lazy(object):
    def __init__(self, name, *args, **kwargs):
        # type (str, *Any, **Any) -> NoReturn
        self.name = name
        self.args = args
        self.kwargs = kwargs
        super(Lazy, self).__init__()
