import six


class _ImmutableContainerType(type):
    """
    Metaclass for immutable container. Creating an immutable container class gives modified init and setattr
    methods. It is meant to be directly created; setting this as __metaclass__ will result in undefined behavior.
    """
    def __init__(cls, name, bases, dct):
        super(_ImmutableContainerType, cls).__init__(name, bases, dct)
        attributes = dct.get('attributes', [])
        strict = dct.get('strict', True)
        cls.__init__ = cls.__class__.make_initializer(attributes, strict)
        cls.__setattr__ = cls.__class__.make_setattr(attributes)
        cls.__repr__ = cls.__class__.make_repr(name)

    @classmethod
    def make_initializer(mcs, attributes, strict):
        """
        Create the init method for the class

        :param attributes: the list of attributes (strings) to accept in the constructor as keyword args
        :return: a modified version of the init method that will accept any keyword args so long as they
        were specified in the list of attributes
        """
        def initializer(self, *_, **kwargs):
            if strict and any(attr not in attributes for attr in kwargs.keys()):
                raise ValueError("Unknown attributes specified for class %s" % self.__class__.__name__)
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
                raise AttributeError("Property %s is immutable" % name)
            super(self.__class__, self).__setattr__(name, value)
        return setter

    @classmethod
    def make_repr(mcs, class_name):
        """
        Create the repr method for the class.

        :param: class_name the name of the class created
        :return: repr version that shows the class name and attribute names and values
        """
        def representation(self):
            sorted_attributes = sorted(six.iteritems(self.__dict__), key=lambda e: e[0])
            attributes = ['%s=%s' % (attr, repr(value)) for attr, value in sorted_attributes]
            attributes_representation = ', '.join(attributes)
            return '%s(%s)' % (class_name, attributes_representation)
        return representation


def _make_container(container_name, attributes, allow_others=False):
    """
    Create a container class.

    :param container_name: the name of the container class
    :type container_name: basestring
    :param attributes: strings, each representing a property on instances of the container class
    :type attributes: basestring, list
    :return: An immutable container class with the specified attributes
    """
    def _get_attributes():
        if not isinstance(attributes, list):
            try:
                return attributes.split(' ')
            except AttributeError:
                raise TypeError("Invalid attributes. Use either a list or space delimited string")
        else:
            return attributes

    def _validate_container_name():
        if not isinstance(container_name, six.string_types):
            raise TypeError("Container name must be a string")
        if not container_name:
            raise ValueError("Empty container name")

    def _validate_attributes(attrs):
        if not all(isinstance(attr, six.string_types) for attr in attrs):
            raise TypeError("All attributes must be strings")

    attributes = _get_attributes()
    _validate_container_name()
    _validate_attributes(attributes)
    params = dict(attributes=attributes, strict=(not allow_others))
    return _ImmutableContainerType(container_name, (object,), params)


ImmutableContainer = _make_container
