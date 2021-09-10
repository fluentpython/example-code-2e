"""
Testing ``Flavor``::

    >>> Flavor.cocoa, Flavor.coconut, Flavor.vanilla
    (0, 1, 2)
    >>> Flavor[1]
    'coconut'

"""

from microenum import MicroEnum


class Flavor(MicroEnum):
    cocoa
    coconut
    vanilla
