class _ImmutableContainerType(type):
    def __new__(mcs, name, bases, dct):
        return super(_ImmutableContainerType, mcs).__new__(mcs, name, bases, dct)

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


class _ImmutableContainer(object):
    """
    example usage:

    RequestModel = ImmutableContainer('RequestModel', 'signature', 'user_id')

    u = User('jonathan')
    rm = RequestModel('test_signature', u)
    print rm.signature  # prints 'test_signature'
    rm.signature = 'another_signature'  # raises AttributeError
    print rm.password  # raises AttributeError

    # Or, without specifying all parameters
    ResponseModel = ImmutableContainer('ResponseModel', 'message', 'code')
    response = ResponseModel(message='success')
    response.status  # returns None
    """
    __metaclass__ = _ImmutableContainerType

    def __call__(self, name, *args, **_):
        return _ImmutableContainerType(name, (object,), dict(attributes=[attr for attr in args]))

ImmutableContainer = _ImmutableContainer()