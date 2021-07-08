"""
``Coordinate``: a simple class with a custom ``__str__``::

    >>> moscow = Coordinate(55.756, 37.617)
    >>> print(moscow)  # doctest:+ELLIPSIS
    <coordinates.Coordinate object at 0x...>
"""

# tag::COORDINATE[]
class Coordinate:

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

# end::COORDINATE[]