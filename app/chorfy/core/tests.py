from django.test import TestCase


class CoreTestCase(TestCase):

    def test_foo(self):
        self.assertEqual("foo", "foo")
