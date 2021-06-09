import random
from typing import Iterable, Generic, TypeVar, TYPE_CHECKING

T_co = TypeVar('T_co', covariant=True)

from generic_randompick import RandomPicker


class LottoPicker(Generic[T_co]):
    def __init__(self, items: Iterable[T_co]) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self) -> T_co:
        return self._items.pop()


def test_issubclass() -> None:
    assert issubclass(LottoPicker, RandomPicker)


def test_isinstance() -> None:
    popper: RandomPicker = LottoPicker[int]([1])
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