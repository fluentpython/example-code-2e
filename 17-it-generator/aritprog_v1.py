"""
Arithmetic progression class

# tag::ARITPROG_CLASS_DEMO[]

    >>> ap = ArithmeticProgression(0, 1, 3)
    >>> list(ap)
    [0, 1, 2]
    >>> ap = ArithmeticProgression(1, .5, 3)
    >>> list(ap)
    [1.0, 1.5, 2.0, 2.5]
    >>> ap = ArithmeticProgression(0, 1/3, 1)
    >>> list(ap)
    [0.0, 0.3333333333333333, 0.6666666666666666]
    >>> from fractions import Fraction
    >>> ap = ArithmeticProgression(0, Fraction(1, 3), 1)
    >>> list(ap)
    [Fraction(0, 1), Fraction(1, 3), Fraction(2, 3)]
    >>> from decimal import Decimal
    >>> ap = ArithmeticProgression(0, Decimal('.1'), .3)
    >>> list(ap)
    [Decimal('0'), Decimal('0.1'), Decimal('0.2')]

# end::ARITPROG_CLASS_DEMO[]
"""


# tag::ARITPROG_CLASS[]
class ArithmeticProgression:

    def __init__(self, begin, step, end=None):       # <1>
        self.begin = begin
        self.step = step
        self.end = end  # None -> "infinite" series

    def __iter__(self):
        result_type = type(self.begin + self.step)   # <2>
        result = result_type(self.begin)             # <3>
        forever = self.end is None                   # <4>
        index = 0
        while forever or result < self.end:          # <5>
            yield result                             # <6>
            index += 1
            result = self.begin + self.step * index  # <7>
# end::ARITPROG_CLASS[]
