from randompop import RandomPopper
import random
from typing import Any, Iterable, TYPE_CHECKING


class SimplePopper:
    def __init__(self, items: Iterable) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pop_random(self) -> Any:
        return self._items.pop()


def test_issubclass() -> None:
    assert issubclass(SimplePopper, RandomPopper)


def test_isinstance() -> None:
    popper: RandomPopper = SimplePopper([1])
    if TYPE_CHECKING:
        reveal_type(popper)
        # Revealed type is 'randompop.RandomPopper'
    assert isinstance(popper, RandomPopper)
