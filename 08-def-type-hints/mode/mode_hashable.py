# tag::MODE_HASHABLE_T[]
from collections import Counter
from collections.abc import Iterable, Hashable
from typing import TypeVar

HashableT = TypeVar('HashableT', bound=Hashable)

def mode(data: Iterable[HashableT]) -> HashableT:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]
# end::MODE_HASHABLE_T[]


def demo() -> None:
    import typing

    pop = 'abracadabra'
    m = mode(pop)
    if typing.TYPE_CHECKING:
        reveal_type(pop)
        reveal_type(m)
    print(pop)
    print(m.upper(), type(m))


if __name__ == '__main__':
    demo()
