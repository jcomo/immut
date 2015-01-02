class _ImmutableContainerType(type):
    def __init__(cls, name, bases, dct):
        super(_ImmutableContainerType, cls).__init__(name, bases, dct)
        cls._attributes = dct.get('attributes', [])
        cls.__init__ = cls.__get_initializer()
        cls.__setattr__ = cls.__get_setattr()

    def __get_initializer(cls):
        def initializer(self, *_, **kwargs):
            if any(attr not in cls._attributes for attr in kwargs.keys()):
                raise ValueError("Unknown attributes specified in constructor for class {}".format(cls.__name__))
            for attr in cls._attributes:
                value = kwargs.get(attr, None)
                self.__dict__[attr] = value
        return initializer

    def __get_setattr(cls):
        def setter(self, name, value):
            if name in cls._attributes:
                raise AttributeError("Property {} is immutable".format(name))
            super(cls, self).__setattr__(name, value)
        return setter


def _make_container(container_name, *attributes):
    return _ImmutableContainerType(container_name, (object,), dict(attributes=[attr for attr in attributes]))


ImmutableContainer = _make_container