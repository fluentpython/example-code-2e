# tag::DOCTESTS[]
"""
``HackerClubMember`` objects accept an optional ``handle`` argument::

    >>> anna = HackerClubMember('Anna Ravenscroft', handle='AnnaRaven')
    >>> anna
    HackerClubMember(name='Anna Ravenscroft', guests=[], handle='AnnaRaven')

If ``handle`` is omitted, it's set to the first part of the member's name::

    >>> leo = HackerClubMember('Leo Rochael')
    >>> leo
    HackerClubMember(name='Leo Rochael', guests=[], handle='Leo')

Members must have a unique handle. The following ``leo2`` will not be created,
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
from club import ClubMember

@dataclass
class HackerClubMember(ClubMember):                         # <1>
    all_handles = set()                                     # <2>
    handle: str = ''                                        # <3>

    def __post_init__(self):
        cls = self.__class__                                # <4>
        if self.handle == '':                               # <5>
            self.handle = self.name.split()[0]
        if self.handle in cls.all_handles:                  # <6>
            msg = f'handle {self.handle!r} already exists.'
            raise ValueError(msg)
        cls.all_handles.add(self.handle)                    # <7>
# end::HACKERCLUB[]
