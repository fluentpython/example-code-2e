from collections import Counter
from typing import Iterable, TypeVar

T = TypeVar('T')

def mode(data: Iterable[T]) -> T:
    data = iter(data)
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]


def demo() -> None:
    from typing import List, Set, TYPE_CHECKING
    pop:List[Set] = [set(), set()]
    m = mode(pop)
    if TYPE_CHECKING:
        reveal_type(pop)
        reveal_type(m)
    print(pop)
    print(repr(m), type(m))

if __name__ == '__main__':
    demo()