import random
from typing import Any, Iterable

from randompickload import LoadableRandomPicker

class SimplePicker:
    def __init__(self, items: Iterable) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self) -> Any:
        return self._items.pop()

class LoadablePicker:  # <1>
    def __init__(self, items: Iterable) -> None:
        self.load(items)

    def pick(self) -> Any:  # <2>
        return self._items.pop()

    def load(self, items: Iterable) -> Any:  # <3>
        self._items = list(items)
        random.shuffle(self._items)

def test_isinstance() -> None:  # <4>
    popper = LoadablePicker([1])
    assert isinstance(popper, LoadableRandomPicker)

def test_isinstance_not() -> None:  # <5>
    popper = SimplePicker([1])
    assert not isinstance(popper, LoadableRandomPicker)

