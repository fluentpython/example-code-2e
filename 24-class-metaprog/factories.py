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
    (<class 'factories.Dog'>, <class 'object'>)

# end::RECORD_FACTORY_DEMO[]

The factory also accepts a list or tuple of identifiers:

    >>> Dog = record_factory('Dog', ['name', 'weight', 'owner'])
    >>> Dog.__slots__
    ('name', 'weight', 'owner')

"""


# tag::RECORD_FACTORY[]
from typing import Union, Any
from collections.abc import Iterable, Iterator

FieldNames = Union[str, Iterable[str]]  # <1>

def record_factory(cls_name: str, field_names: FieldNames) -> type[tuple]:  # <2>

    slots = parse_identifiers(field_names)  # <3>

    def __init__(self, *args, **kwargs) -> None:  # <4>
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self) -> Iterator[Any]:  # <5>
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):  # <6>
        values = ', '.join(f'{name}={value!r}'
            for name, value in zip(self.__slots__, self))
        cls_name = self.__class__.__name__
        return f'{cls_name}({values})'

    cls_attrs = dict(  # <7>
        __slots__=slots,
        __init__=__init__,
        __iter__=__iter__,
        __repr__=__repr__,
    )

    return type(cls_name, (object,), cls_attrs)  # <8>


def parse_identifiers(names: FieldNames) -> tuple[str, ...]:
    if isinstance(names, str):
        names = names.replace(',', ' ').split()  # <9>
    if not all(s.isidentifier() for s in names):
        raise ValueError('names must all be valid identifiers')
    return tuple(names)
# end::RECORD_FACTORY[]
