import typing

class Coordinate(typing.NamedTuple):
    lat: float
    lon: float

trash = Coordinate('Ni!', None)  # <1>
print(trash)
