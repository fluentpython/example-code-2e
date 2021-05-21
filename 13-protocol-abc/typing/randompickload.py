from typing import Protocol, runtime_checkable
from randompick import RandomPicker

@runtime_checkable  # <1>
class LoadableRandomPicker(RandomPicker, Protocol):  # <2>
    def load(self, Iterable) -> None: ...  # <3>
