"""
A coroutine to compute a running average.

Testing ``averager2`` by itself::

# tag::RETURNING_AVERAGER_DEMO_1[]

    >>> coro_avg = averager2()
    >>> next(coro_avg)
    >>> coro_avg.send(10)  # <1>
    >>> coro_avg.send(30)
    >>> coro_avg.send(6.5)
    >>> coro_avg.close()  # <2>

# end::RETURNING_AVERAGER_DEMO_1[]

Catching `StopIteration` to extract the value returned by
the coroutine::

# tag::RETURNING_AVERAGER_DEMO_2[]

    >>> coro_avg = averager2()
    >>> next(coro_avg)
    >>> coro_avg.send(10)
    >>> coro_avg.send(30)
    >>> coro_avg.send(6.5)
    >>> try:
    ...     coro_avg.send(STOP)  # <1>
    ... except StopIteration as exc:
    ...     result = exc.value  # <2>
    ...
    >>> result  # <3>
    Result(count=3, average=15.5)

# end::RETURNING_AVERAGER_DEMO_2[]

Using `yield from`:


# tag::RETURNING_AVERAGER_DEMO_3[]

    >>> def compute():
    ...     res = yield from averager2(True)  # <1>
    ...     print('computed:', res)  # <2>
    ...     return res  # <3>
    ...
    >>> comp = compute()  # <4>
    >>> for v in [None, 10, 20, 30, STOP]:  # <5>
    ...     try:
    ...         comp.send(v)  # <6>
    ...     except StopIteration as exc:  # <7>
    ...         result = exc.value
    received: 10
    received: 20
    received: 30
    received: <Sentinel>
    computed: Result(count=3, average=20.0)
    >>> result  # <8>
    Result(count=3, average=20.0)

# end::RETURNING_AVERAGER_DEMO_3[]
"""

# tag::RETURNING_AVERAGER_TOP[]
from collections.abc import Generator
from typing import Union, NamedTuple

class Result(NamedTuple):  # <1>
    count: int  # type: ignore  # <2>
    average: float

class Sentinel:  # <3>
    def __repr__(self):
        return f'<Sentinel>'

STOP = Sentinel()  # <4>

SendType = Union[float, Sentinel]  # <5>
# end::RETURNING_AVERAGER_TOP[]
# tag::RETURNING_AVERAGER[]
def averager2(verbose: bool = False) -> Generator[None, SendType, Result]:  # <1>
    total = 0.0
    count = 0
    average = 0.0
    while True:
        term = yield  # <2>
        if verbose:
            print('received:', term)
        if isinstance(term, Sentinel):  # <3>
            break
        total += term  # <4>
        count += 1
        average = total / count
    return Result(count, average)  # <5>

# end::RETURNING_AVERAGER[]
