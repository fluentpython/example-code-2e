from typing import Protocol, runtime_checkable, TypeVar

T_co = TypeVar('T_co', covariant=True)  # <1>

@runtime_checkable
class RandomPicker(Protocol[T_co]):  # <2>
    def pick(self) -> T_co: ...  # <3>
