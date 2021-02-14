"""
``top(it, n)`` returns the "greatest" ``n`` elements of the iterable ``t``.
Example:

# tag::TOP_DOCTEST[]
>>> top([4, 1, 5, 2, 6, 7, 3], 3)
[7, 6, 5]
>>> l = 'mango pear apple kiwi banana'.split()
>>> top(l, 3)
['pear', 'mango', 'kiwi']
>>>
>>> l2 = [(len(s), s) for s in l]
>>> l2
[(5, 'mango'), (4, 'pear'), (5, 'apple'), (4, 'kiwi'), (6, 'banana')]
>>> top(l2, 3)
[(6, 'banana'), (5, 'mango'), (5, 'apple')]

# end::TOP_DOCTEST[]

"""

# tag::TOP[]
from typing import TypeVar, Iterable, List
from comparable import Comparable

CT = TypeVar('CT', bound=Comparable)

def top(series: Iterable[CT], length: int) -> List[CT]:
    return sorted(series, reverse=True)[:length]
# end::TOP[]
