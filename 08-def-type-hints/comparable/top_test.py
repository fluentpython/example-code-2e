from typing import Tuple, List, Iterator, TYPE_CHECKING
import pytest # type: ignore
from top import top

@pytest.mark.parametrize('series, length, expected', [
    ((1, 2, 3), 2, [3, 2]),
    ((1, 2, 3), 3, [3, 2, 1]),
    ((3, 3, 3), 1, [3]),
])
def test_top(
    series: Tuple[float, ...],
    length: int,
    expected: List[float],
) -> None:
    result = top(series, length)
    assert expected == result

# tag::TOP_TEST[]
def test_top_tuples() -> None:
    fruit = 'mango pear apple kiwi banana'.split()
    series: Iterator[Tuple[int, str]] = (
        (len(s), s) for s in fruit)
    length = 3
    expected = [(6, 'banana'), (5, 'mango'), (5, 'apple')]
    result = top(series, length)
    if TYPE_CHECKING:
        reveal_type(series)
        reveal_type(expected)
        reveal_type(result)
    assert result == expected

# intentional type error
def test_top_objects_error() -> None:
    series = [object() for _ in range(4)]
    if TYPE_CHECKING:
        reveal_type(series)
    with pytest.raises(TypeError) as exc:
        top(series, 3)
    assert "'<' not supported" in str(exc)
# end::TOP_TEST[]
