"""
Short demos
===========

``UpperDict`` behaves like a case-insensitive mapping`::

# tag::UPPERDICT_DEMO[]
    >>> d = UpperDict([('a', 'letter A'), (2, 'digit two')])
    >>> list(d.keys())
    ['A', 2]
    >>> d['b'] = 'letter B'
    >>> 'b' in d
    True
    >>> d['a'], d.get('B')
    ('letter A', 'letter B')
    >>> list(d.keys())
    ['A', 2, 'B']

# end::UPPERDICT_DEMO[]

And ``UpperCounter`` is also case-insensitive::

# tag::UPPERCOUNTER_DEMO[]
    >>> c = UpperCounter('BaNanA')
    >>> c.most_common()
    [('A', 3), ('N', 2), ('B', 1)]

# end::UPPERCOUNTER_DEMO[]

Detailed tests
==============

UpperDict uppercases all string keys.

    >>> d = UpperDict([('a', 'letter A'), ('B', 'letter B'), (2, 'digit two')])


Tests for item retrieval using `d[key]` notation::

    >>> d['A']
    'letter A'
    >>> d['b']
    'letter B'
    >>> d[2]
    'digit two'


Tests for missing key::

    >>> d['z']
    Traceback (most recent call last):
      ...
    KeyError: 'Z'
    >>> d[99]
    Traceback (most recent call last):
      ...
    KeyError: 99


Tests for item retrieval using `d.get(key)` notation::

    >>> d.get('a')
    'letter A'
    >>> d.get('B')
    'letter B'
    >>> d.get(2)
    'digit two'
    >>> d.get('z', '(not found)')
    '(not found)'

Tests for the `in` operator::

    >>> ('a' in d, 'B' in d, 'z' in d)
    (True, True, False)

Test for item assignment using lowercase key::

    >>> d['c'] = 'letter C'
    >>> d['C']
    'letter C'

Tests for update using a `dict` or a sequence of pairs::

    >>> d.update({'D': 'letter D', 'e': 'letter E'})
    >>> list(d.keys())
    ['A', 'B', 2, 'C', 'D', 'E']
    >>> d.update([('f', 'letter F'), ('G', 'letter G')])
    >>> list(d.keys())
    ['A', 'B', 2, 'C', 'D', 'E', 'F', 'G']
    >>> d  # doctest:+NORMALIZE_WHITESPACE
    {'A': 'letter A', 'B': 'letter B', 2: 'digit two',
    'C': 'letter C', 'D': 'letter D', 'E': 'letter E',
    'F': 'letter F', 'G': 'letter G'}

UpperCounter uppercases all `str` keys.

Test for initializer: keys are uppercased.

    >>> d = UpperCounter('AbracAdaBrA')
    >>> sorted(d.keys())
    ['A', 'B', 'C', 'D', 'R']

Tests for count retrieval using `d[key]` notation::

    >>> d['a']
    5
    >>> d['z']
    0

"""
# tag::UPPERCASE_MIXIN[]
import collections

def _upper(key):  # <1>
    try:
        return key.upper()
    except AttributeError:
        return key

class UpperCaseMixin:  # <2>
    def __setitem__(self, key, item):
        super().__setitem__(_upper(key), item)

    def __getitem__(self, key):
        return super().__getitem__(_upper(key))

    def get(self, key, default=None):
        return super().get(_upper(key), default)

    def __contains__(self, key):
        return super().__contains__(_upper(key))
# end::UPPERCASE_MIXIN[]

# tag::UPPERDICT[]
class UpperDict(UpperCaseMixin, collections.UserDict):  # <1>
    pass

class UpperCounter(UpperCaseMixin, collections.Counter):  # <2>
    """Specialized 'Counter' that uppercases string keys"""  # <3>
# end::UPPERDICT[]
