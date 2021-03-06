from nose.tools import eq_

from functools import partial
from ddtrace.utils.importlib import func_name
from ddtrace.utils.formats import asbool


class SomethingCallable(object):
    """
    A dummy class that implements __call__().
    """
    value = 42

    def __call__(self):
        return 'something'

    def me(self):
        return self

    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def answer(cls):
        return cls.value


def some_function():
    """
    A function doing nothing.
    """
    return 'nothing'

def minus(a,b):
    return a - b

minus_two = partial(minus, b=2) # partial funcs need special handling (no module)

# disabling flake8 test below, yes, declaring a func like this is bad, we know
plus_three = lambda x : x + 3  # NOQA

class TestContrib(object):
    """
    Ensure that contrib utility functions handles corner cases
    """
    def test_func_name(self):
        # check that func_name works on anything callable, not only funcs.
        eq_('nothing', some_function())
        eq_('tests.contrib.test_utils.some_function', func_name(some_function))

        f = SomethingCallable()
        eq_('something', f())
        eq_('tests.contrib.test_utils.SomethingCallable', func_name(f))

        eq_(f, f.me())
        eq_('tests.contrib.test_utils.me', func_name(f.me))
        eq_(3, f.add(1,2))
        eq_('tests.contrib.test_utils.add', func_name(f.add))
        eq_(42, f.answer())
        eq_('tests.contrib.test_utils.answer', func_name(f.answer))

        eq_('tests.contrib.test_utils.minus', func_name(minus))
        eq_(5, minus_two(7))
        eq_('partial', func_name(minus_two))
        eq_(10, plus_three(7))
        eq_('tests.contrib.test_utils.<lambda>', func_name(plus_three))
