from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class RandomPopper(Protocol):
    def pop_random(self) -> Any: ...
