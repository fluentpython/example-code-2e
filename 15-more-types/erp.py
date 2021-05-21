import random
from typing import TypeVar, Generic, List, Iterable


T = TypeVar('T')


class EnterpriserRandomPopper(Generic[T]):
    def __init__(self, items: Iterable[T]) -> None:
        self._items: List[T] = list(items)
        random.shuffle(self._items)

    def pop_random(self) -> T:
        return self._items.pop()
