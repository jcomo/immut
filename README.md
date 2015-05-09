# Immut
An immutable container library for Python

![](https://travis-ci.org/jcomo/immut.svg?branch=master)

## Use case
The intended use case for this library is to create named immutable container classes
to use in an application. This would be particularly useful for value objects. Create
an immutable container to hold a bunch of data with named fields and pass it freely
around the application knowing that the contents will not be modified after creation.


## Example usage
```
pip install immut
```

```python
from immut import ImmutableContainer

ResponseModel = ImmutableContainer('ResponseModel', 'message', 'code')
response = ResponseModel(message='success')
response.message  # returns 'success'
response.code  # returns None

# The fields can be anything
u = User('jonathan')
RequestModel = ImmutableContainer('RequestModel', 'user')
request = RequestModel(user=u)
```


## API
The sole API is for creating a container.

```python
ImmutableContainer(container_name, *fields)
```

**Parameters**
* `container_name` the name of the class for the container (string). Generally, simply set it to the name of the variable
you are assigning to.
* `fields` each field is a string representing the fields that this container will have

**Returns**
A dynamically generated immutable container

**Behavior**
* Trying to set a specified field on the immutable container after creation will raise an `AttributeError`.
* Setting a *non-specified* field in the constructor will raise a `ValueError`
  * Setting a non-specified field on the container after construction is allowed, but is not recommended as it is
  outside the scope of the use case and is bad python programming practice in general.
* Non-initialized fields in the constructor will return `None` when accessed.


### Disclaimer
I know this isn't the most pythonic or useful library in the world. It was conceived
as a way for me to learn how meta classes work. However, it has its uses, and it is
well tested.

##### Differences with `collections.namedtuple`
There are many similarities with this library and `collections.namedtuple`. The main difference is in the behavior with initialization. With a namedtuple, each defined attribute must be initialized in the constructor but with this container library, attributes are initialized to None by default if they are unspecified in the constructor.
