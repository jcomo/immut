class _ImmutableContainerType(type):
    def __init__(cls, name, bases, dct):
        super(_ImmutableContainerType, cls).__init__(name, bases, dct)
        attributes = dct.get('attributes', [])
        cls.__init__ = cls.__class__.make_initializer(attributes)
        cls.__setattr__ = cls.__class__.make_setattr(attributes)

    @classmethod
    def make_initializer(mcs, attributes):
        def initializer(self, *_, **kwargs):
            if any(attr not in attributes for attr in kwargs.keys()):
                raise ValueError("Unknown attributes specified for class {}".format(self.__class__.__name__))
            for attr in attributes:
                value = kwargs.get(attr, None)
                self.__dict__[attr] = value
        return initializer

    @classmethod
    def make_setattr(mcs, attributes):
        def setter(self, name, value):
            if name in attributes:
                raise AttributeError("Property {} is immutable".format(name))
            super(self.__class__, self).__setattr__(name, value)
        return setter


def _make_container(container_name, *attributes):
    if not isinstance(container_name, basestring):
        raise TypeError("Container name must be a string")
    if not container_name:
        raise ValueError("Empty container name")
    if not all(isinstance(attr, basestring) for attr in attributes):
        raise TypeError("All attributes must be strings")
    return _ImmutableContainerType(container_name, (object,), dict(attributes=[attr for attr in attributes]))


ImmutableContainer = _make_container