"""
Media resource description class with subset of the Dublin Core fields.

Default field values:

    >>> r = Resource('0')
    >>> r  # doctest: +NORMALIZE_WHITESPACE
    Resource(identifier='0', title='<untitled>', creators=[], date=None,
    type=<ResourceType.BOOK: 1>, description='', language='', subjects=[])

A complete resource record:
# tag::DOCTEST[]

    >>> description = 'Improving the design of existing code'
    >>> book = Resource('978-0-13-475759-9', 'Refactoring, 2nd Edition',
    ...     ['Martin Fowler', 'Kent Beck'], date(2018, 11, 19),
    ...     ResourceType.BOOK, description, 'EN',
    ...     ['computer programming', 'OOP'])
    >>> book  # doctest: +NORMALIZE_WHITESPACE
    Resource(identifier='978-0-13-475759-9', title='Refactoring, 2nd Edition',
    creators=['Martin Fowler', 'Kent Beck'], date=datetime.date(2018, 11, 19),
    type=<ResourceType.BOOK: 1>, description='Improving the design of existing code',
    language='EN', subjects=['computer programming', 'OOP'])

# end::DOCTEST[]
"""

# tag::DATACLASS[]
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum, auto
from datetime import date


class ResourceType(Enum):  # <1>
    BOOK = auto()
    EBOOK = auto()
    VIDEO = auto()


@dataclass
class Resource:
    """Media resource description."""
    identifier: str                                    # <2>
    title: str = '<untitled>'                          # <3>
    creators: list[str] = field(default_factory=list)
    date: Optional[date] = None                        # <4>
    type: ResourceType = ResourceType.BOOK             # <5>
    description: str = ''
    language: str = ''
    subjects: list[str] = field(default_factory=list)
# end::DATACLASS[]


from typing import TypedDict


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
