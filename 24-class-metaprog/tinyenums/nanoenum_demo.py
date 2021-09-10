"""
Testing ``Flavor``::

    >>> Flavor.coconut
    'coconut'
    >>> Flavor.cocoa, Flavor.vanilla
    ('cocoa', 'vanilla')

"""

from nanoenum import NanoEnum


class Flavor(NanoEnum):
    cocoa
    coconut
    vanilla
