# This example requires the geolib library:
# https://pypi.org/project/geolib/


"""
>>> shanghai = 31.2304, 121.4737
>>> geohash(shanghai)
'wtw3sjq6q'
"""

# tag::GEOHASH[]
from typing import NamedTuple

from geolib import geohash as gh  # type: ignore

PRECISION = 9

class Coordinate(NamedTuple):
    lat: float
    lon: float

def geohash(lat_lon: Coordinate) -> str:
    return gh.encode(*lat_lon, PRECISION)
# end::GEOHASH[]

# tag::DISPLAY[]
def display(lat_lon: tuple[float, float]) -> str:
    lat, lon = lat_lon
    ns = 'N' if lat >= 0 else 'S'
    ew = 'E' if lon >= 0 else 'W'
    return f'{abs(lat):0.1f}°{ns}, {abs(lon):0.1f}°{ew}'
# end::DISPLAY[]

def demo():
    shanghai = 31.2304, 121.4737
    print(display(shanghai))
    s = geohash(shanghai)
    print(s)

if __name__ == '__main__':
    demo()
