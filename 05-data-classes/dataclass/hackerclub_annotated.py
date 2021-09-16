# tag::DOCTESTS[]
"""
``HackerClubMember`` objects can be created with a ``name`` and an optional ``handle``::

    >>> anna = HackerClubMember('Anna Ravenscroft', handle='AnnaRaven')
    >>> anna
    HackerClubMember(name='Anna Ravenscroft', guests=[], handle='AnnaRaven')

If ``handle`` is omitted, it's set to the first part of the member's name::

    >>> leo = HackerClubMember('Leo Rochael')
    >>> leo
    HackerClubMember(name='Leo Rochael', guests=[], handle='Leo')

Members must have a unique handle. This ``leo2`` will not be created,
because its ``handle`` would be 'Leo', which was taken by ``leo``::

    >>> leo2 = HackerClubMember('Leo DaVinci')
    Traceback (most recent call last):
      ...
    ValueError: handle 'Leo' already exists.

To fix, ``leo2`` must be created with an explicit ``handle``::

    >>> leo2 = HackerClubMember('Leo DaVinci', handle='Neo')
    >>> leo2
    HackerClubMember(name='Leo DaVinci', guests=[], handle='Neo')
"""
# end::DOCTESTS[]

# tag::HACKERCLUB[]
from dataclasses import dataclass
from typing import ClassVar
from club import ClubMember

@dataclass
class HackerClubMember(ClubMember):
    all_handles: ClassVar[set[str]] = set()
    handle: str = ''

    def __post_init__(self):
        cls = self.__class__
        if self.handle == '':
            self.handle = self.name.split()[0]
        if self.handle in cls.all_handles:
            msg = f'handle {self.handle!r} already exists.'
            raise ValueError(msg)
        cls.all_handles.add(self.handle)
# end::HACKERCLUB[]
