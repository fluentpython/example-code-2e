"""
======================
AddableBingoCage tests
======================


Tests for __add__:

# tag::ADDABLE_BINGO_ADD_DEMO[]

    >>> vowels = 'AEIOU'
    >>> globe = AddableBingoCage(vowels)  # <1>
    >>> globe.inspect()
    ('A', 'E', 'I', 'O', 'U')
    >>> globe.pick() in vowels  # <2>
    True
    >>> len(globe.inspect())  # <3>
    4
    >>> globe2 = AddableBingoCage('XYZ')  # <4>
    >>> globe3 = globe + globe2
    >>> len(globe3.inspect())  # <5>
    7
    >>> void = globe + [10, 20]  # <6>
    Traceback (most recent call last):
      ...
    TypeError: unsupported operand type(s) for +: 'AddableBingoCage' and 'list'


# end::ADDABLE_BINGO_ADD_DEMO[]

Tests for __iadd__:

# tag::ADDABLE_BINGO_IADD_DEMO[]

    >>> globe_orig = globe  # <1>
    >>> len(globe.inspect())  # <2>
    4
    >>> globe += globe2  # <3>
    >>> len(globe.inspect())
    7
    >>> globe += ['M', 'N']  # <4>
    >>> len(globe.inspect())
    9
    >>> globe is globe_orig  # <5>
    True
    >>> globe += 1  # <6>
    Traceback (most recent call last):
      ...
    TypeError: right operand in += must be 'Tombola' or an iterable

# end::ADDABLE_BINGO_IADD_DEMO[]

"""

# tag::ADDABLE_BINGO[]
from tombola import Tombola
from bingo import BingoCage


class AddableBingoCage(BingoCage):  # <1>

    def __add__(self, other):
        if isinstance(other, Tombola):  # <2>
            return AddableBingoCage(self.inspect() + other.inspect())
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Tombola):
            other_iterable = other.inspect()  # <3>
        else:
            try:
                other_iterable = iter(other)  # <4>
            except TypeError:  # <5>
                msg = ('right operand in += must be '
                       "'Tombola' or an iterable")
                raise TypeError(msg)
        self.load(other_iterable)  # <6>
        return self  # <7>

# end::ADDABLE_BINGO[]
