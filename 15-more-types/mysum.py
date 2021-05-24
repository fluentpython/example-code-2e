from functools import reduce  # <1>
from operator import add
from typing import overload, Iterable, Union, TypeVar

T = TypeVar('T')
S = TypeVar('S')  # <2>

@overload
def sum(it: Iterable[T]) -> Union[T, int]: ...  # <3>
@overload
def sum(it: Iterable[T], /, start: S) -> Union[T, S]: ...  # <4>
def sum(it, /, start=0):  # <5>
    return reduce(add, it, start)
