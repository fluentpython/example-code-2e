"""
bisect_demo.py

Demonstration of ``bisect.bisect``::

    >>> import bisect
    >>> demo(bisect.bisect)
    31 @ 14      |  |  |  |  |  |  |  |  |  |  |  |  |  |31
    30 @ 14      |  |  |  |  |  |  |  |  |  |  |  |  |  |30
    29 @ 13      |  |  |  |  |  |  |  |  |  |  |  |  |29
    23 @ 11      |  |  |  |  |  |  |  |  |  |  |23
    22 @  9      |  |  |  |  |  |  |  |  |22
    10 @  5      |  |  |  |  |10
     8 @  5      |  |  |  |  |8
     5 @  3      |  |  |5
     2 @  1      |2
     1 @  1      |1
     0 @  0    0


Demonstration of ``bisect.bisect_left``::

    >>> demo(bisect.bisect_left)
    31 @ 14      |  |  |  |  |  |  |  |  |  |  |  |  |  |31
    30 @ 13      |  |  |  |  |  |  |  |  |  |  |  |  |30
    29 @ 12      |  |  |  |  |  |  |  |  |  |  |  |29
    23 @  9      |  |  |  |  |  |  |  |  |23
    22 @  9      |  |  |  |  |  |  |  |  |22
    10 @  5      |  |  |  |  |10
     8 @  4      |  |  |  |8
     5 @  2      |  |5
     2 @  1      |2
     1 @  0    1
     0 @  0    0


"""

# tag::BISECT_DEMO[]
import bisect
import sys

HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]

ROW_FMT = '{0:2d} @ {1:2d}    {2}{0:<2d}'

def demo(bisect_fn):
    for needle in reversed(NEEDLES):
        position = bisect_fn(HAYSTACK, needle)  # <1>
        offset = position * '  |'  # <2>
        print(ROW_FMT.format(needle, position, offset))  # <3>

if __name__ == '__main__':

    if sys.argv[-1] == 'left':    # <4>
        bisect_fn = bisect.bisect_left
    else:
        bisect_fn = bisect.bisect

    print('DEMO:', bisect_fn.__name__)  # <5>
    print('haystack ->', ' '.join(f'{n:2}' for n in HAYSTACK))
    demo(bisect_fn)

# end::BISECT_DEMO[]
