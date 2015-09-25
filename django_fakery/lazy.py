class Lazy(object):
    def __init__(self, field_name):
        self.field_name = field_name
        super(Lazy, self).__init__()
