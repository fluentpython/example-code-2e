#!/usr/bin/env python3

"""
Testing ``WilyDict``::

    >>> from autoconst import WilyDict
    >>> wd = WilyDict()
    >>> len(wd)
    0
    >>> wd['first']
    0
    >>> wd
    {'first': 0}
    >>> wd['second']
    1
    >>> wd['third']
    2
    >>> len(wd)
    3
    >>> wd
    {'first': 0, 'second': 1, 'third': 2}
    >>> wd['__magic__']
    Traceback (most recent call last):
      ...
    KeyError: '__magic__'

Testing ``AutoConst``::

    >>> from autoconst import AutoConst

# tag::AUTOCONST[]
    >>> class Flavor(AutoConst):
    ...     banana
    ...     coconut
    ...     vanilla
    ...
    >>> Flavor.vanilla
    2
    >>> Flavor.banana, Flavor.coconut
    (0, 1)

# end::AUTOCONST[]

"""

from autoconst import AutoConst


class Flavor(AutoConst):
    banana
    coconut
    vanilla


print('Flavor.vanilla ==', Flavor.vanilla)