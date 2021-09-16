"""
A coroutine to compute a running average

# tag::CORO_AVERAGER_TEST[]
    >>> coro_avg = averager()  # <1>
    >>> next(coro_avg)  # <2>
    0.0
    >>> coro_avg.send(10)  # <3>
    10.0
    >>> coro_avg.send(30)
    20.0
    >>> coro_avg.send(5)
    15.0

# end::CORO_AVERAGER_TEST[]
# tag::CORO_AVERAGER_TEST_CONT[]

    >>> coro_avg.send(20)  # <1>
    16.25
    >>> coro_avg.close()  # <2>
    >>> coro_avg.close()  # <3>
    >>> coro_avg.send(5)  # <4>
    Traceback (most recent call last):
      ...
    StopIteration

# end::CORO_AVERAGER_TEST_CONT[]

"""

# tag::CORO_AVERAGER[]
from collections.abc import Generator

def averager() -> Generator[float, float, None]:  # <1>
    total = 0.0
    count = 0
    average = 0.0
    while True:  # <2>
        term = yield average  # <3>
        total += term
        count += 1
        average = total/count
# end::CORO_AVERAGER[]
