import typing

class Coordinate(typing.NamedTuple):

    lat: float
    lon: float

trash = Coordinate('foo', None)  # <1>
print(trash)
