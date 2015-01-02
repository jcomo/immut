class _ImmutableContainerType(type):
    """
    Metaclass for immutable container. Creating an immutable container class gives modified init and setattr
    methods. It is meant to be directly created; setting this as __metaclass__ will result in undefined behavior.
    """
    def __init__(cls, name, bases, dct):
        super(_ImmutableContainerType, cls).__init__(name, bases, dct)
        attributes = dct.get('attributes', [])
        cls.__init__ = cls.__class__.make_initializer(attributes)
        cls.__setattr__ = cls.__class__.make_setattr(attributes)

    @classmethod
    def make_initializer(mcs, attributes):
        """
        Create the init method for the class

        :param attributes: the list of attributes (strings) to accept in the constructor as keyword args
        :return: a modified version of the init method that will accept any keyword args so long as they
        were specified in the list of attributes
        """
        def initializer(self, *_, **kwargs):
            if any(attr not in attributes for attr in kwargs.keys()):
                raise ValueError("Unknown attributes specified for class {}".format(self.__class__.__name__))
            for attr in attributes:
                value = kwargs.get(attr, None)
                self.__dict__[attr] = value
        return initializer

    @classmethod
    def make_setattr(mcs, attributes):
        """
        Create the setattr method for the class. This version of setattr will raise an AttributeError when trying
        to set any of the specified immutable attributes

        :param attributes: a list of attributes (strings) to make immutable
        :return: a modified version of the setattr method that keeps the specified attributes immutable
        """
        def setter(self, name, value):
            if name in attributes:
                raise AttributeError("Property {} is immutable".format(name))
            super(self.__class__, self).__setattr__(name, value)
        return setter


def _make_container(container_name, *attributes):
    """
    Create a container class.

    :param container_name: the name of the container class
    :type container_name: basestring
    :param attributes: strings, each representing a property on instances of the container class
    :type attributes: basestring
    :return: An immutable container class with the specified attributes
    """
    if not isinstance(container_name, basestring):
        raise TypeError("Container name must be a string")
    if not container_name:
        raise ValueError("Empty container name")
    if not all(isinstance(attr, basestring) for attr in attributes):
        raise TypeError("All attributes must be strings")
    return _ImmutableContainerType(container_name, (object,), dict(attributes=[attr for attr in attributes]))


ImmutableContainer = _make_container