"""
match_cities.py
"""

# tag::CITY[]
import typing

class City(typing.NamedTuple):
    continent: str
    name: str
    country: str


cities = [
    City('Asia', 'Tokyo', 'JP'),
    City('Asia', 'Delhi', 'IN'),
    City('North America', 'Mexico City', 'MX'),
    City('North America', 'New York', 'US'),
    City('South America', 'São Paulo', 'BR'),
]
# end::CITY[]

# tag::ASIA[]
def match_asian_cities():
    results = []
    for city in cities:
        match city:
            case City(continent='Asia'):
                results.append(city)
    return results
# end::ASIA[]

# tag::ASIA_POSITIONAL[]
def match_asian_cities_pos():
    results = []
    for city in cities:
        match city:
            case City('Asia'):
                results.append(city)
    return results
# end::ASIA_POSITIONAL[]


# tag::ASIA_COUNTRIES[]
def match_asian_countries():
    results = []
    for city in cities:
        match city:
            case City(continent='Asia', country=cc):
                results.append(cc)
    return results
# end::ASIA_COUNTRIES[]

# tag::ASIA_COUNTRIES_POSITIONAL[]
def match_asian_countries_pos():
    results = []
    for city in cities:
        match city:
            case City('Asia', _, country):
                results.append(country)
    return results
# end::ASIA_COUNTRIES_POSITIONAL[]


def match_india():
    results = []
    for city in cities:
        match city:
            case City(_, name, 'IN'):
                results.append(name)
    return results


def match_brazil():
    results = []
    for city in cities:
        match city:
            case City(country='BR', name=name):
                results.append(name)
    return results



def main():
    tests = ((n, f) for n, f in globals().items() if n.startswith('match_'))

    for name, func in tests:
        print(f'{name:15}\t{func()}')


if __name__ == '__main__':
    main()
