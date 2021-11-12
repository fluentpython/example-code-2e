
"""
Could this be valid Python?

    if now >= T[4:20:PM]: chill()


>>> t = T[4:20]
>>> t
T[4:20]
>>> h, m, s = t
>>> h, m, s
(4, 20, 0)
>>> t[11:59:AM]
T[11:59:AM]
>>> start = t[9:O1:PM]
>>> start
T[9:O1:PM]
>>> start.h, start.m, start.s, start.pm
(9, 1, 0, True)
>>> now = T[7:O1:PM]
>>> T[4:OO:PM]
T[4:OO:PM]
>>> now > T[4:20:PM]
True
"""

import functools

AM = -2
PM = -1

for n in range(10):
    globals()[f'O{n}'] = n
OO = 0

@functools.total_ordering
class T():

    def __init__(self, arg):
        if isinstance(arg, slice):
            h = arg.start or 0
            m = arg.stop or 0
            s = arg.step or 0
        else:
            h, m, s = 0, 0, arg
        if m in (AM, PM):
            self.pm = m == PM
            m = 0
        elif s in (AM, PM):
            self.pm = s == PM
            s = 0
        else:
            self.pm = None
        self.h, self.m, self.s = h, m, s

    def __class_getitem__(cls, arg):
        return cls(arg)

    def __getitem__(self, arg):
        return(type(self)(arg))

    def __repr__(self):
        h, m, s = self.h, self.m, self.s or None
        if m == 0:
            m = f'OO'
        elif m < 10:
            m = f'O{m}'
        s = '' if s is None else s
        if self.pm is None:
            pm = ''
        else:
            pm = ':' + ('AM', 'PM')[self.pm]
        return f'T[{h}:{m}{s}{pm}]'

    def __iter__(self):
        yield from (self.h, self.m, self.s)

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __lt__(self, other):
        return tuple(self) < tuple(other)

    def __add__(self, other):
        """
        >>> T[11:O5:AM] + 15  # TODO: preserve pm field
        T[11:20]
        """
        if isinstance(other, int):
            return self[self.h:self.m + other:self.pm]
