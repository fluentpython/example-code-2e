"""
Media resource description class with subset of the Dublin Core fields.

Default field values:

    >>> r = Resource('0')
    >>> r  # doctest: +NORMALIZE_WHITESPACE
    Resource(
        identifier = '0',
        title = '<untitled>',
        creators = [],
        date = None,
        type = <ResourceType.BOOK: 1>,
        description = '',
        language = '',
        subjects = [],
    )

A complete resource record:

    >>> description = 'Improving the design of existing code'
    >>> book = Resource('978-0-13-475759-9', 'Refactoring, 2nd Edition',
    ...     ['Martin Fowler', 'Kent Beck'], date(2018, 11, 19),
    ...     ResourceType.BOOK, description, 'EN',
    ...     ['computer programming', 'OOP'])

# tag::DOCTEST[]
    >>> book  # doctest: +NORMALIZE_WHITESPACE
    Resource(
        identifier = '978-0-13-475759-9',
        title = 'Refactoring, 2nd Edition',
        creators = ['Martin Fowler', 'Kent Beck'],
        date = datetime.date(2018, 11, 19),
        type = <ResourceType.BOOK: 1>,
        description = 'Improving the design of existing code',
        language = 'EN',
        subjects = ['computer programming', 'OOP'],
    )

# end::DOCTEST[]
"""

from dataclasses import dataclass, field, fields
from typing import Optional, TypedDict
from enum import Enum, auto
from datetime import date


class ResourceType(Enum):
    BOOK = auto()
    EBOOK = auto()
    VIDEO = auto()


@dataclass
class Resource:
    """Media resource description."""
    identifier: str
    title: str = '<untitled>'
    creators: list[str] = field(default_factory=list)
    date: Optional[date] = None
    type: ResourceType = ResourceType.BOOK
    description: str = ''
    language: str = ''
    subjects: list[str] = field(default_factory=list)

# tag::REPR[]
    def __repr__(self):
        cls = self.__class__
        cls_name = cls.__name__
        indent = ' ' * 4
        res = [f'{cls_name}(']                            # <1>
        for f in fields(cls):                             # <2>
            value = getattr(self, f.name)                 # <3>
            res.append(f'{indent}{f.name} = {value!r},')  # <4>

        res.append(')')                                   # <5>
        return '\n'.join(res)                             # <6>
# end::REPR[]


class ResourceDict(TypedDict):
    identifier: str
    title: str
    creators: list[str]
    date: Optional[date]
    type: ResourceType
    description: str
    language: str
    subjects: list[str]


if __name__ == '__main__':
    r = Resource('0')
    description = 'Improving the design of existing code'
    book = Resource('978-0-13-475759-9', 'Refactoring, 2nd Edition',
                    ['Martin Fowler', 'Kent Beck'], date(2018, 11, 19),
                    ResourceType.BOOK, description,
                    'EN', ['computer programming', 'OOP'])
    print(book)
    book_dict: ResourceDict = {
        'identifier': '978-0-13-475759-9',
        'title': 'Refactoring, 2nd Edition',
        'creators': ['Martin Fowler', 'Kent Beck'],
        'date': date(2018, 11, 19),
        'type': ResourceType.BOOK,
        'description': 'Improving the design of existing code',
        'language': 'EN',
        'subjects': ['computer programming', 'OOP']}
    book2 = Resource(**book_dict)
    print(book == book2)
