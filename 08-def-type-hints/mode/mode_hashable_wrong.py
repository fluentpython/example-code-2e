# tag::MODE_FLOAT[]
from collections import Counter
from typing import Iterable, Hashable

def mode(data: Iterable[Hashable]) -> Hashable:
    data = iter(data)
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]
# end::MODE_FLOAT[]

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