import random

from collections.abc import Iterable
from typing import TypeVar, Generic

from tombola import Tombola

T = TypeVar('T')

class LottoBlower(Tombola, Generic[T]):  # <1>

    def __init__(self, items: Iterable[T]) -> None:  # <2>
        self._balls = list[T](items)

    def load(self, items: Iterable[T]) -> None:  # <3>
        self._balls.extend(items)

    def pick(self) -> T:  # <4>
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LottoBlower')
        return self._balls.pop(position)

    def loaded(self) -> bool:  # <5>
        return bool(self._balls)

    def inspect(self) -> tuple[T, ...]:  # <6>
        return tuple(self._balls)
