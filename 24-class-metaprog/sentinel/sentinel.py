"""
This module provides a ``Sentinel`` class that can be used directly as a
sentinel singleton, or subclassed if a distinct sentinel singleton is needed.

The ``repr`` of a ``Sentinel`` class is its name::

    >>> class Missing(Sentinel): pass
    >>> Missing
    Missing

If a different ``repr`` is required,
you can define it as a class attribute::

    >>> class CustomRepr(Sentinel):
    ...     repr = '<CustomRepr>'
    ...
    >>> CustomRepr
    <CustomRepr>

``Sentinel`` classes cannot be instantiated::

    >>> Missing()
    Traceback (most recent call last):
      ...
    TypeError: 'Missing' is a sentinel and cannot be instantiated

"""


class _SentinelMeta(type):
    def __repr__(cls):
        try:
            return cls.repr
        except AttributeError:
            return cls.__name__


class Sentinel(metaclass=_SentinelMeta):
    def __new__(cls):
        msg = 'is a sentinel and cannot be instantiated'
        raise TypeError(f"'{cls!r}' {msg}")
