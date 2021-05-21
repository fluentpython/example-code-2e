"""
record_factory: create simple classes just for holding data fields

# tag::RECORD_FACTORY_DEMO[]
    >>> Dog = record_factory('Dog', 'name weight owner')  # <1>
    >>> rex = Dog('Rex', 30, 'Bob')
    >>> rex  # <2>
    Dog(name='Rex', weight=30, owner='Bob')
    >>> name, weight, _ = rex  # <3>
    >>> name, weight
    ('Rex', 30)
    >>> "{2}'s dog weighs {1}kg".format(*rex)  # <4>
    "Bob's dog weighs 30kg"
    >>> rex.weight = 32  # <5>
    >>> rex
    Dog(name='Rex', weight=32, owner='Bob')
    >>> Dog.__mro__  # <6>
    (<class 'factories_ducktyped.Dog'>, <class 'object'>)

# end::RECORD_FACTORY_DEMO[]

The factory also accepts a list or tuple of identifiers:

    >>> Dog = record_factory('Dog', ['name', 'weight', 'owner'])
    >>> Dog.__slots__
    ('name', 'weight', 'owner')

"""


# tag::RECORD_FACTORY[]
from typing import Union, Any
from collections.abc import Sequence, Iterator

FieldNames = Union[str, Sequence[str]]


def parse_identifiers(names):
    try:
        names = names.replace(',', ' ').split()  # <1>
    except AttributeError:  # no .replace or .split
        pass  # assume it's already a sequence of strings
    if not all(s.isidentifier() for s in names):
        raise ValueError('names must all be valid identifiers')
    return tuple(names)


def record_factory(cls_name, field_names):

    field_identifiers = parse_identifiers(field_names)

    def __init__(self, *args, **kwargs) -> None:  # <4>
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self) -> Iterator[Any]:  # <5>
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):  # <6>
        values = ', '.join(
            '{}={!r}'.format(*i) for i in zip(self.__slots__, self)
        )
        cls_name = self.__class__.__name__
        return f'{cls_name}({values})'

    cls_attrs = dict(
        __slots__=field_identifiers,  # <7>
        __init__=__init__,
        __iter__=__iter__,
        __repr__=__repr__,
    )

    return type(cls_name, (object,), cls_attrs)  # <8>


# end::RECORD_FACTORY[]
