import random
from typing import Iterable, TYPE_CHECKING

from randompick_generic import GenericRandomPicker


class LottoPicker():
    def __init__(self, items: Iterable[int]) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self) -> int:
        return self._items.pop()


def test_issubclass() -> None:
    assert issubclass(LottoPicker, GenericRandomPicker)


def test_isinstance() -> None:
    popper: GenericRandomPicker = LottoPicker([1])
    if TYPE_CHECKING:
        reveal_type(popper)
        # Revealed type is '???'
    assert isinstance(popper, LottoPicker)


def test_pick_type() -> None:
    balls = [1, 2, 3]
    popper = LottoPicker(balls)
    pick = popper.pick()
    assert pick in balls
    if TYPE_CHECKING:
        reveal_type(pick)
        # Revealed type is '???'