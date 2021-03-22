from typing import Protocol, runtime_checkable, TypeVar

T_co = TypeVar('T_co', covariant=True)

@runtime_checkable
class GenericRandomPicker(Protocol[T_co]):
    def pick(self) -> T_co: ...
