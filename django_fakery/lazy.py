from typing import Any


class Lazy(object):
    def __init__(self, name, *args, **kwargs):
        # type (str, *Any, **Any) -> None
        self.name = name
        self.args = args
        self.kwargs = kwargs
        super(Lazy, self).__init__()
