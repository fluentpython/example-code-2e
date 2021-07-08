"""
metro_lat_lon.py

Demonstration of nested tuple unpacking::

    >>> main()
                    |  latitude | longitude
    Mexico City     |   19.4333 |  -99.1333
    New York-Newark |   40.8086 |  -74.0204
    São Paulo       |  -23.5478 |  -46.6358

"""

# tag::MAIN[]
metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),  # <1>
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

def main():
    print(f'{"":15} | {"latitude":>9} | {"longitude":>9}')
    for name, _, _, (lat, lon) in metro_areas:  # <2>
        if lon <= 0:  # <3>
            print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')

if __name__ == '__main__':
    main()
# end::MAIN[]