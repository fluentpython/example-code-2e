"""
``Coordinate``: simple class decorated with ``dataclass`` and a custom ``__str__``::

    >>> moscow = Coordinate(55.756, 37.617)
    >>> print(moscow)
    55.8°N, 37.6°E

"""

# tag::COORDINATE[]

from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
	
    lat: float
    long: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.long >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.long):.1f}°{we}'
# end::COORDINATE[]