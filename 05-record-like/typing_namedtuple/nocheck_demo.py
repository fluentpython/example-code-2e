import typing

class Coordinate(typing.NamedTuple):

    lat: float
    long: float

trash = Coordinate('foo', None)  # <1>
print(trash)                           
