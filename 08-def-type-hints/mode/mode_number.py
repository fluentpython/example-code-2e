from collections import Counter
from typing import Iterable, TypeVar
from decimal import Decimal
from fractions import Fraction

NumberT = TypeVar('NumberT', float, Decimal, Fraction)

def mode(data: Iterable[NumberT]) -> NumberT:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]


def demo() -> None:
    from typing import TYPE_CHECKING
    pop = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 2)]
    m = mode(pop)
    if TYPE_CHECKING:
        reveal_type(pop)
        reveal_type(m)
    print(pop)
    print(repr(m), type(m))

if __name__ == '__main__':
    demo()