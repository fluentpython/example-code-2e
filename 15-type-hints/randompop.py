from typing import Protocol, TypeVar, runtime_checkable, Any


@runtime_checkable
class RandomPopper(Protocol):
    def pop_random(self) -> Any: ...
