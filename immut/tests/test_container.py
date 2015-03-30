import unittest
from immut import ImmutableContainer


class ContainerTestCase(unittest.TestCase):
    def test_empty_container(self):
        Container = ImmutableContainer('Container', [])
        c = Container()
        self.assertRaises(AttributeError, getattr, c, 'something')

    def test_container_with_one_attribute(self):
        Container = ImmutableContainer('Container', 'message')
        c = Container(message='hello')
        self.assertEquals(c.message, 'hello')

    def test_container_raises_for_invalid_attribute(self):
        Container = ImmutableContainer('Container', 'message')
        self.assertRaises(ValueError, Container, message='hello', unspecified=True)

    def test_container_cannot_set_values(self):
        Container = ImmutableContainer('Container', 'message')
        c = Container(message='hello')
        self.assertRaises(AttributeError, setattr, c, 'message', 'hey')

    def test_container_can_set_values_for_invalid_attributes(self):
        Container = ImmutableContainer('Container', 'message')
        c = Container()
        try:
            c.unspecified = True
        except (AttributeError, ValueError, KeyError):
            self.fail("Should be able to set unspecified properties")

    def test_container_with_multiple_values(self):
        Container = ImmutableContainer('Container', ['message', 'status', 'user'])
        message = 'success'
        status = 0
        user = type('User', (object,), dict())

        c = Container(message=message, status=status, user=user)
        self.assertEquals(c.message, message)
        self.assertEquals(c.status, status)
        self.assertEquals(c.user, user)

    def test_container_with_multiple_values_optional(self):
        Container = ImmutableContainer('Container', ['message', 'status', 'user'])
        message = 'success'
        user = type('User', (object,), dict())

        c = Container(message=message, user=user)
        self.assertEquals(c.message, message)
        self.assertEquals(c.user, user)
        self.assertEquals(c.status, None)

    def test_container_with_others_allowed_flag(self):
        Container = ImmutableContainer('Container', 'message', allow_others=True)
        message = 'success'

        try:
            c = Container(message=message, user=object())
        except ValueError:
            self.fail("Should be able to create with arbitrary arguments")

        self.assertEquals(c.message, message)

    def test_container_with_space_delimited_attributed(self):
        Container = ImmutableContainer('Container', 'message user')
        message = 'success'
        user = object()

        c = Container(message=message, user=user)

        self.assertEquals(c.message, message)
        self.assertEquals(c.user, user)

    def test_bad_class_names_dont_collide(self):
        Container1 = ImmutableContainer('Container', 'message')
        Container2 = ImmutableContainer('Container', [])

        c1 = Container1(message='hi')
        c2 = Container2()

        self.assertEquals(c1.message, 'hi')
        self.assertRaises(AttributeError, getattr, c2, 'message')

    def test_container_error_messages(self):
        self.assertRaisesRegexp(
            ValueError, r"Empty container name",
            ImmutableContainer, '', [])
        self.assertRaisesRegexp(
            TypeError, r"Container name must be a string",
            ImmutableContainer, 0, [])
        self.assertRaisesRegexp(
            TypeError, r"Invalid attributes. Use either a list or space delimited string",
            ImmutableContainer, 'TestContainer', 0)
        self.assertRaisesRegexp(
            TypeError, r"All attributes must be strings",
            ImmutableContainer, 'TestContainer', [0])

    def test_setter_error_messages(self):
        TestContainer = ImmutableContainer('TestContainer', 'message')
        c = TestContainer(message='hi')
        try:
            c.message = 'hey'
            self.fail("Expected AttributeError")
        except AttributeError as e:
            self.assertEquals(e.message, "Property message is immutable")

    def test_constructor_error_messages(self):
        TestContainer = ImmutableContainer('TestContainer', 'message')
        try:
            TestContainer(status=0)
            self.fail("Expected ValueError")
        except ValueError as e:
            self.assertEquals(e.message, "Unknown attributes specified for class TestContainer")