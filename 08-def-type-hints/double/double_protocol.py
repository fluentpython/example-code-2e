from typing import TypeVar, Protocol

T = TypeVar('T')  # <1>

class Repeatable(Protocol):
    def __mul__(self: T, other: int) -> T: ...  # <2>

RT = TypeVar('RT', bound=Repeatable)  # <3>

def double(n: RT) -> RT:  # <4>
    return n * 2
