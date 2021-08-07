# tag::MODE_FLOAT[]
from collections import Counter
from collections.abc import Iterable

def mode(data: Iterable[float]) -> float:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]
# end::MODE_FLOAT[]

def demo() -> None:
    import typing
    pop = [1, 1, 2, 3, 3, 3, 3, 4]
    m = mode(pop)
    if typing.TYPE_CHECKING:
        reveal_type(pop)
        reveal_type(m)
    print(pop)
    print(repr(m), type(m))

if __name__ == '__main__':
    demo()
