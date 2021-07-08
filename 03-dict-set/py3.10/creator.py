"""
Pattern matching with mapping—requires Python ≥ 3.10

# tag::DICT_MATCH_TEST[]
>>> b1 = dict(api=1, author='Douglas Hofstadter',
...         type='book', title='Gödel, Escher, Bach')
>>> get_creators(b1)
['Douglas Hofstadter']
>>> from collections import OrderedDict
>>> b2 = OrderedDict(api=2, type='book',
...         title='Python in a Nutshell',
...         authors='Martelli Ravenscroft Holden'.split())
>>> get_creators(b2)
['Martelli', 'Ravenscroft', 'Holden']
>>> get_creators({'type': 'book', 'pages': 770})
Traceback (most recent call last):
    ...
ValueError: Invalid 'book' record: {'type': 'book', 'pages': 770}
>>> get_creators('Spam, spam, spam')
Traceback (most recent call last):
    ...
ValueError: Invalid record: 'Spam, spam, spam'

# end::DICT_MATCH_TEST[]
"""

# tag::DICT_MATCH[]
def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:  # <1>
            return names
        case {'type': 'book', 'api': 1, 'author': name}:  # <2>
            return [name]
        case {'type': 'book'}:  # <3>
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:  # <4>
            return [name]
        case _:  # <5>
            raise ValueError(f'Invalid record: {record!r}')
# end::DICT_MATCH[]
