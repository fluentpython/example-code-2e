# tag::SAMPLE[]
from collections.abc import Sequence
from random import shuffle
from typing import TypeVar

T = TypeVar('T')

def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
        raise ValueError('size must be >= 1')
    result = list(population)
    shuffle(result)
    return result[:size]
# end::SAMPLE[]

def demo() -> None:
    import typing
    p1 = tuple(range(10))
    s1 = sample(p1, 3)
    if typing.TYPE_CHECKING:
        reveal_type(p1)
        reveal_type(s1)
    print(p1)
    print(s1)
    p2 = 'The quick brown fox jumps over the lazy dog'
    s2 = sample(p2, 10)
    if typing.TYPE_CHECKING:
        reveal_type(p2)
        reveal_type(s2)
    print(p2)
    print(s2)


if __name__ == '__main__':
    demo()
