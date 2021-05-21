"""
Example adapted from `Atomic Kotlin` by Bruce Eckel & Svetlana Isakova,
chapter `Creating Generics`, section `Variance`.
"""

from typing import TypeVar, Generic, Any


class Pet:
    """Domestic animal kept for companionship."""


class Cat(Pet):
    """Felis catus"""


class Siamese(Cat):
    """Cat breed from Thailand"""


T = TypeVar('T')


class Box(Generic[T]):
    def put(self, item: T) -> None:
        self.contents = item

    def get(self) -> T:
        return self.contents


T_co = TypeVar('T_co', covariant=True)


class OutBox(Generic[T_co]):
    def __init__(self, contents: Any):
        self.contents = contents

    def get(self) -> Any:
        return self.contents


T_contra = TypeVar('T_contra', contravariant=True)


class InBox(Generic[T_contra]):
    def put(self, item: T) -> None:
        self.contents = item
