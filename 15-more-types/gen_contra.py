"""
In ``Generator[YieldType, SendType, ReturnType]``,
``SendType`` is contravariant.
The other type variables are covariant.

This is how ``typing.Generator`` is declared::

    class Generator(Iterator[T_co], Generic[T_co, T_contra, V_co]):

(from https://docs.python.org/3/library/typing.html#typing.Generator)

"""

from typing import Generator


# Generator[YieldType, SendType, ReturnType]

def gen_float_take_int() -> Generator[float, int, str]:
    received = yield -1.0
    while received:
        received = yield float(received)
    return 'Done'


def gen_float_take_float() -> Generator[float, float, str]:
    received = yield -1.0
    while received:
        received = yield float(received)
    return 'Done'


def gen_float_take_complex() -> Generator[float, complex, str]:
    received = yield -1.0
    while received:
        received = yield abs(received)
    return 'Done'

# Generator[YieldType, SendType, ReturnType]

g0: Generator[float, float, str] = gen_float_take_float()

g1: Generator[complex, float, str] = gen_float_take_float()

## Incompatible types in assignment
##   expression has type "Generator[float, float, str]"
##     variable has type "Generator[int, float, str]")
# g2: Generator[int, float, str] = gen_float_take_float()


# Generator[YieldType, SendType, ReturnType]

g3: Generator[float, int, str] = gen_float_take_float()

## Incompatible types in assignment
##   expression has type "Generator[float, float, str]"
##     variable has type "Generator[float, complex, str]")
## g4: Generator[float, complex, str] = gen_float_take_float()

