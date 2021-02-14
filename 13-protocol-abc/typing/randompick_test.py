import random
from typing import Any, Iterable, TYPE_CHECKING

from randompick import RandomPicker  # <1>

class SimplePicker():  # <2>
    def __init__(self, items: Iterable) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self) -> Any:  # <3>
        return self._items.pop()

def test_isinstance() -> None:  # <4>
    popper = SimplePicker([1])
    assert isinstance(popper, RandomPicker)

def test_item_type() -> None:  # <5>
    items = [1, 2]
    popper = SimplePicker(items)
    item = popper.pick()
    assert item in items
    if TYPE_CHECKING:
        reveal_type(item)  # <6>
    assert isinstance(item, int)
